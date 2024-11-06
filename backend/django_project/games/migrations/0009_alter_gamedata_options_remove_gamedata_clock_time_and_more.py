# Generated by Django 5.1 on 2024-09-12 23:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_remove_gamedata_game_remove_gamedata_timestamp_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamedata',
            options={'verbose_name': 'Строка данных игрока', 'verbose_name_plural': 'Данные игрока'},
        ),
        migrations.RemoveField(
            model_name='gamedata',
            name='clock_time',
        ),
        migrations.AlterField(
            model_name='game',
            name='match_id',
            field=models.IntegerField(help_text='ID игры, присвоенный Dota', unique=True, verbose_name='Идентификатор игры'),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_player', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]