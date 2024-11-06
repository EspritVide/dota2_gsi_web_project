import asyncio
import json
from datetime import datetime
from typing import Union

from .constants import (REQUIRED_GSI_STRUCTURE,
                        GAME_STATES_CONTINUE,
                        GSI_KEYS_FOR_DELETE,
                        TIME_FOR_PLAYER_FAIL)
from .exceptions import UserGsiTokenError
from django_project.scripts import get_redis_client
from games.models import Game, Player
from users.models import User
from ws.scripts import ws_group_send_message


def get_cleared_gsi_data(json_obj: str) -> Union[bool, dict]:
    """
    Get GSI data from request in json.\n
    If data isnt valid json obj or doesnt match structure - return False.
    """
    cleared_gsi_data = {}
    try:
        gsi_data = json.loads(json_obj)
    except json.JSONDecodeError:
        return False
    for main_key in REQUIRED_GSI_STRUCTURE:
        if main_key not in gsi_data.keys():
            return False
        else:
            cleared_gsi_data[main_key] = {}
            for sub_key in REQUIRED_GSI_STRUCTURE[main_key]:
                gsi_obj = gsi_data[main_key].get(sub_key, None)
                if gsi_obj is None:
                    return False
                else:
                    if not type(gsi_obj) is REQUIRED_GSI_STRUCTURE[main_key][sub_key]:
                        return False
                    cleared_gsi_data[main_key][sub_key] = gsi_obj
    return cleared_gsi_data


def delete_useless_gsi_data(gsi_data: dict) -> dict:
    """Removes unnecessary information from GSI data."""
    for key, second_keys in GSI_KEYS_FOR_DELETE.items():
        if second_keys is None:
            del gsi_data[key]
        else:
            for second_key in second_keys:
                try:
                    del gsi_data[key][second_key]
                except KeyError:
                    pass
    return gsi_data


def check_continue_condition(gsi_data: dict) -> bool:
    """Check GSI Data and return True if data should be processed."""
    game_state = gsi_data['map']['game_state']
    player_activity = gsi_data['player']['activity']
    is_paused = gsi_data['map']['paused']
    return (game_state in GAME_STATES_CONTINUE
            and player_activity == 'playing'
            and not is_paused)


def validate_player(gsi_data: dict) -> dict:
    """
    Return player pk and whether or not player should be added in game.\n
    If player doesnt exist in Redis - check user in DB.\n
    If user of player doesnt exist in DB - set player_pk to 'DONT_EXIST'
    and raise UserGsiTokenError.
    """
    result = {'req_add_in_game': False}

    match_id = gsi_data['map']['matchid']
    gsi_token = gsi_data['auth']['token']
    timestamp = gsi_data['provider']['timestamp']
    player_key = f'gsi:player:{match_id}:{gsi_token}'

    r = get_redis_client()
    player_pk = r.hget(player_key, 'player_pk')
    if player_pk is None:
        user = User.objects.filter(gsi_token__value=gsi_token).first()
        if user:
            hero = gsi_data['hero']['name']
            team = gsi_data['player']['team_name']
            player = Player.objects.create(user=user, hero=hero, team=team, status='playing')
            player_pk = player.pk
            result['req_add_in_game'] = True
        else:
            r.hmset(player_key, {'timestamp': timestamp, 'player_pk': 'DONT_EXIST'})
            raise UserGsiTokenError(gsi_token)
    elif player_pk == 'DONT_EXIST':
        raise UserGsiTokenError(gsi_token)

    result['player_pk'] = int(player_pk)
    return result


def set_player(game_pk: int, player_pk: int, gsi_data: dict) -> None:
    """
    Add player to game.players in DB.\n
    Create player with pk in Redis.\n
    Add player.pk to game[player_pks] in Redis.
    """
    Game.add_player(game_pk, player_pk)

    match_id = gsi_data['map']['matchid']
    gsi_token = gsi_data['auth']['token']
    timestamp = gsi_data['provider']['timestamp']
    player_key = f'gsi:player:{match_id}:{gsi_token}'
    r = get_redis_client()

    r.hmset(player_key, {'timestamp': timestamp, 'player_pk': player_pk})

    game_key = f'gsi:game:{match_id}'
    players_pks = json.loads(r.hget(game_key, 'player_pks'))
    players_pks.append(player_pk)
    r.hset(game_key, 'player_pks', json.dumps(players_pks))

    user_pk = Player.objects.get(pk=player_pk).user.pk
    group_name = f'games_list_{user_pk}'
    asyncio.run(
        ws_group_send_message(group_name, 'new_game_created', {'game_pk': game_pk})
    )


def set_game_data(player_pk: int, gsi_data: dict) -> None:
    """
    Write game data to Redis.\n
    Refresh timestamp for game in Redis.
    """
    r = get_redis_client()

    timestamp = gsi_data['provider']['timestamp']
    match_id = int(gsi_data['map']['matchid'])
    clock_time = gsi_data['map']['clock_time']
    gsi_token = gsi_data['auth']['token']

    data_key = f'gsi:game_data:{player_pk}:{timestamp}'
    usefull_gsi_data = delete_useless_gsi_data(gsi_data)
    r.set(data_key, json.dumps(usefull_gsi_data))
    r.hmset(f'gsi:game:{match_id}', {'timestamp': timestamp, 'clock_time': clock_time})
    r.hmset(f'gsi:player:{match_id}:{gsi_token}', {'timestamp': timestamp})

    user_pk = Player.objects.get(pk=player_pk).user.pk
    game_pk = Game.objects.get(match_id=match_id).pk
    group_name = f'game_detail_{game_pk}_{user_pk}'
    asyncio.run(
        ws_group_send_message(group_name, 'new_game_data', {'gsi_data': gsi_data})
    )


def open_game(gsi_data: dict) -> int:
    """
    Create game in DB and Redis.\n
    Return game pk.
    """
    match_id = int(gsi_data['map']['matchid'])
    game = Game.objects.create(match_id=match_id, status='opened')

    game_key = f'gsi:game:{match_id}'
    timestamp = gsi_data['provider']['timestamp']
    r = get_redis_client()
    r.hmset(game_key,
            {'game_pk': game.pk,
             'timestamp': timestamp,
             'player_pks': json.dumps([]), }
            )

    return game.pk


def close_game(match_id: int,
               win_team: str = '',
               clock_time: int = None,
               failed: bool = False, ) -> None:
    """
    Change status of game, players
    and set duration, win_team for game in DB.\n
    Delete game, players keys related to game in Redis.
    """
    r = get_redis_client()
    game_key = f'gsi:game:{match_id}'

    if failed:
        game_status = 'failed'
        clock_time = r.hget(game_key, 'clock_time')
    else:
        game_status = 'closed'
        clock_time = clock_time
    Game.objects.filter(match_id=match_id).update(
        status=game_status,
        duration=clock_time,
        win_team=win_team, )

    current_timestamp = datetime.now().timestamp()
    player_keys = r.keys(f'gsi:player:{match_id}:*')
    for key in player_keys:
        player_pk = int(r.hget(key, 'player_pk'))
        timestamp = int(r.hget(key, 'timestamp'))
        difference = current_timestamp - timestamp
        if difference >= TIME_FOR_PLAYER_FAIL:
            player_status = 'failed'
        else:
            player_status = 'ended'
        Player.objects.filter(pk=player_pk).update(status=player_status)

        user_pk = Player.objects.get(pk=player_pk).user.pk
        game_pk = Game.objects.get(match_id=match_id).pk
        group_name = f'games_list_{user_pk}'
        asyncio.run(
            ws_group_send_message(group_name, 'game_change_status', {'game_pk': game_pk})
        )

    redis_keys_for_delete = player_keys
    redis_keys_for_delete.append(game_key)
    r.delete(*redis_keys_for_delete)
