from django.db import models

from users.models import User


TEAMS = (
    ('dire', 'Dire'),
    ('radiant', 'Radiant'),
)


class Player(models.Model):
    PLAYER_STATUSES = (
            ('playing', 'Играет'),
            ('ended', 'Завершил'),
            ('failed', 'Недостаточная информация'),
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='as_player',
        on_delete=models.CASCADE,
    )
    team = models.CharField(
        verbose_name='Команда',
        max_length=10,
        choices=TEAMS,
    )
    hero = models.CharField(
        verbose_name='Герой',
        max_length=100,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=10,
        choices=PLAYER_STATUSES,
    )

    def __str__(self):
        return f'Герой - {self.hero}. Статус - {self.status}.'

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class Game(models.Model):
    GAME_STATUSES = (
            ('opened', 'Открыта'),
            ('closed', 'Завершена'),
            ('failed', 'Недостаточная информация'),
    )
    match_id = models.IntegerField(
        verbose_name='Идентификатор игры',
        help_text='ID игры, присвоенный Dota',
        unique=True,
    )
    datetime = models.DateTimeField(
        verbose_name='Дата игры',
        auto_now_add=True,
        help_text='Дата создания игры в БД'
    )
    win_team = models.CharField(
        verbose_name='Команда победителя',
        max_length=10,
        choices=TEAMS,
        null=True, blank=True,
    )
    duration = models.IntegerField(
        verbose_name='Длительность игры',
        help_text='Длительность игры в секундах',
        null=True, blank=True,
    )
    players = models.ManyToManyField(
        Player,
        verbose_name='Игроки',
        related_name='game',
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=10,
        choices=GAME_STATUSES,
    )

    @classmethod
    def add_player(cls, game_pk: int, player_pk: int, ):
        """Add player to game.players in DB according pk."""
        player = Player.objects.get(id=player_pk)
        game = Game.objects.get(id=game_pk)
        game.players.add(player)

    def __str__(self):
        return f'Игра №{self.match_id}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class GameData(models.Model):
    player = models.ForeignKey(
        Player,
        verbose_name='Игрок',
        related_name='data',
        on_delete=models.CASCADE,
        help_text='Игрок, к которому относится данная информация',
    )
    clock_time = models.IntegerField(
        verbose_name='Время',
        help_text='Время в секундах',
    )
    data = models.JSONField(
        verbose_name='Информация',
        help_text='Получена от GSI',
    )

    @classmethod
    def get_unsaved_obj(cls, player_pk: int, data: dict):
        clock_time = data['map']['clock_time']
        data['map'].pop('clock_time')
        obj = cls(player_id=player_pk,
                  clock_time=clock_time,
                  data=data, )
        return obj

    def __str__(self):
        return f'GSI data игрока: {self.player}'

    class Meta:
        verbose_name = 'Строка данных игрока'
        verbose_name_plural = 'Данные игрока'
