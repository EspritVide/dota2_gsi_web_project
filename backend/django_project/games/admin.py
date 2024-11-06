from django.contrib import admin

from . import models


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'match_id',
        'datetime',
        'duration',
    )
    ordering = (
        '-datetime',
    )


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'team',
        'hero',
    )
    ordering = (
        '-id',
    )


@admin.register(models.GameData)
class GameDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'player',
        'clock_time',
    )
    ordering = (
        '-player__id', '-clock_time',
    )
