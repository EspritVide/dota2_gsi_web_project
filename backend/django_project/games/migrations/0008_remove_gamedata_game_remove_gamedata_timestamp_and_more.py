# Generated by Django 5.1 on 2024-09-10 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_remove_game_players_remove_game_status_game_win_team_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamedata',
            name='game',
        ),
        migrations.RemoveField(
            model_name='gamedata',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='player',
            name='game',
        ),
        migrations.AddField(
            model_name='game',
            name='duration',
            field=models.IntegerField(blank=True, help_text='Длительность игры в секундах', null=True, verbose_name='Длительность игры'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(related_name='game', to='games.player', verbose_name='Игроки'),
        ),
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('opened', 'Открыта'), ('closed', 'Завершена'), ('failed', 'Недостаточная информация')], default='closed', max_length=10, verbose_name='Статус'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gamedata',
            name='clock_time',
            field=models.IntegerField(default=0, help_text='Время в секундах, прошедшее с начала игры', verbose_name='Время игры'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='status',
            field=models.CharField(choices=[('playing', 'Играет'), ('ended', 'Завершил'), ('failed', 'Недостаточная информация')], default='ended', max_length=10, verbose_name='Статус'),
            preserve_default=False,
        ),
    ]