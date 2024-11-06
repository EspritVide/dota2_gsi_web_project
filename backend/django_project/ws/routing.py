from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/games_list/", consumers.GamesListConsumer.as_asgi()),
    re_path(r"ws/game_detail/(?P<game_id>\w+)/$", consumers.GameDetailConsumer.as_asgi()),
]
