import json
from datetime import datetime

from celery import shared_task
from django.db import transaction

from .constants import TIME_FOR_GAME_FAIL
from .scripts import close_game
from django_project.scripts import get_redis_client
from games.models import GameData


@shared_task
def save_game_data() -> int:
    r = get_redis_client()
    keys = r.keys('gsi:game_data:*:*')
    values = r.mget(keys)
    game_data_list = []

    for i, key in enumerate(keys):
        player_pk = key.split(':')[2]
        data = json.loads(values[i])
        game_data_obj = GameData.get_unsaved_obj(player_pk, data)
        game_data_list.append(game_data_obj)

    if game_data_list:
        with transaction.atomic():
            GameData.objects.bulk_create(game_data_list)
            r.delete(*keys)

    return len(game_data_list)


@shared_task
def check_failed_games() -> int:
    r = get_redis_client()
    keys = r.keys('gsi:game:*')
    failed_games_count = 0

    for key in keys:
        timestamp = int(r.hget(key, 'timestamp'))
        current_timestamp = datetime.now().timestamp()
        difference = (current_timestamp - timestamp)
        if difference >= TIME_FOR_GAME_FAIL:
            match_id = key.split(':')[2]
            close_game(match_id, failed=True)
            failed_games_count += 1

    return failed_games_count
