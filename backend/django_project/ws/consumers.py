import json

# from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class GamesListConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f'games_list_{self.user.pk}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def new_game_created(self, event):
        await self.send(text_data=json.dumps(event))

    async def game_change_status(self, event):
        await self.send(text_data=json.dumps(event))


class GameDetailConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.group_name = f'game_detail_{self.game_id}_{self.user.pk}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def new_game_data(self, event):
        await self.send(text_data=json.dumps(event))

    async def game_closed(self, event):
        await self.send(text_data=json.dumps(event), close=True)
