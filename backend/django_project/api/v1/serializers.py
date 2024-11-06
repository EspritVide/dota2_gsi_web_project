from rest_framework import serializers
import json

from games.models import Game, GameData
from django_project.scripts import get_redis_client


class GameSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    hero = serializers.SerializerMethodField()

    def get_result(self, obj) -> str:
        """
        Return result of the player in the game.\n
        Results:
        - opened (game not finished yet)
        - failed (dont enough data for result)
        - win
        - loose
        """
        if obj.status in ('opened', 'failed'):
            return obj.status
        player = obj.players.get(user=self.context['request'].user)
        return 'win' if player.team == obj.win_team else 'loose'

    def get_hero(self, obj):
        return obj.players.get(user=self.context['request'].user).hero

    class Meta:
        model = Game
        fields = ('id',
                  'datetime',
                  'hero',
                  'result',
                  'duration', )


class GameDataSerializator(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        if isinstance(obj.data, dict):
            data = obj.data
        else:
            data = json.loads(obj.data)
        return data

    class Meta:
        model = GameData
        fields = ('clock_time', 'data', )


class GameDetailSerializer(GameSerializer):
    game_data = serializers.SerializerMethodField()

    def get_game_data(self, obj):
        player = obj.players.get(user=self.context['request'].user)
        game_data = player.data.order_by('clock_time').all()
        game_data_serialized = GameDataSerializator(game_data, many=True).data
        if obj.status == 'opened':
            r = get_redis_client()
            keys = r.keys(f'gsi:game_data:{player.pk}:*')
            for value in r.mget(keys):
                data = json.loads(value)
                unsaved_obj = GameData.get_unsaved_obj(player.pk, data)
                game_data_serialized.append(GameDataSerializator(unsaved_obj).data)
        return game_data_serialized

    class Meta(GameSerializer.Meta):
        new_fields = ('match_id', 'game_data')
        fields = GameSerializer.Meta.fields + new_fields
