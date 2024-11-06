from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .constants import GAME_STATE_END
from .decorators import check_gsi_data
from .scripts import (open_game,
                      close_game,
                      validate_player,
                      set_game_data,
                      set_player)
from django_project.scripts import get_redis_client


@require_http_methods(['POST'])
@csrf_exempt
@check_gsi_data
def gsi_reciever(request, gsi_data: dict, ):

    # with open(f'{BASE_DIR}/game_states.txt', mode='a') as f:
    #     f.write(pprint.pformat(gsi_data) + '\n')

    # "gsi:game:{match_id}" - { timestamp:int, clock_time:int, game_pk:int, player_pks:list }
    # "gsi:player:{match_id}:{gsi_token}" - player_pk:int
    # "gsi:game_data:{player_pk}:{timestamp}" - data:dict

    game_state = gsi_data['map']['game_state']
    match_id = int(gsi_data['map']['matchid'])

    game_key = f'gsi:game:{match_id}'
    r = get_redis_client()
    if r.exists(game_key):
        if game_state == GAME_STATE_END:
            close_game(match_id,
                       win_team=gsi_data['map']['win_team'],
                       clock_time=gsi_data['map']['clock_time'], )
        else:
            validate_result = validate_player(gsi_data)
            player_pk = validate_result['player_pk']
            if validate_result['req_add_in_game']:
                game_pk = int(r.hget(game_key, 'game_pk'))
                set_player(game_pk, player_pk, gsi_data)
            set_game_data(player_pk, gsi_data)

    elif game_state != GAME_STATE_END:
        validate_result = validate_player(gsi_data)
        game_pk = open_game(gsi_data)
        player_pk = validate_result['player_pk']
        set_player(game_pk, player_pk, gsi_data)
        set_game_data(player_pk, gsi_data)

    return HttpResponse('OK')
