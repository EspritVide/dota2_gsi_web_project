
# Данный кортеж определяет game_states,
# при которых можно продолжать обработку данных.
GAME_STATES_CONTINUE = (
    'DOTA_GAMERULES_STATE_PRE_GAME',
    'DOTA_GAMERULES_STATE_GAME_IN_PROGRESS',
    'DOTA_GAMERULES_STATE_POST_GAME',
    )

# game_state при котором игра считается законченной
GAME_STATE_END = 'DOTA_GAMERULES_STATE_POST_GAME'

# Структура и типизация которым должна соответствовать gsi_data
REQUIRED_GSI_STRUCTURE = {
    'auth': {
        'token': str
    },
    'hero': {
        # 'aghanims_scepter': bool,
        # 'aghanims_shard': bool,
        # 'alive': bool,
        # 'attributes_level': int,
        # 'break': bool,
        # 'buyback_cooldown': int,
        # 'buyback_cost': int,
        # 'disarmed': bool,
        # 'facet': int,
        # 'has_debuff': bool,
        # 'health': int,
        # 'health_percent': int,
        # 'hexed': bool,
        # 'id': int,
        # 'level': int,
        # 'magicimmune': bool,
        # 'mana': int,
        # 'mana_percent': int,
        # 'max_health': int,
        # 'max_mana': int,
        # 'muted': bool,
        'name': str,
        # 'respawn_seconds': int,
        # 'silenced': bool,
        # 'smoked': bool,
        # 'stunned': bool,
        # 'talent_1': bool,
        # 'talent_2': bool,
        # 'talent_3': bool,
        # 'talent_4': bool,
        # 'talent_5': bool,
        # 'talent_6': bool,
        # 'talent_7': bool,
        # 'talent_8': bool,
        # 'xp': int,
        # 'xpos': int,
        # 'ypos': int
    },
    'map': {
        'clock_time': int,
        # 'customgamename': str,
        # 'daytime': bool,
        # 'dire_score': int,
        'game_state': str,
        # 'game_time': int,
        'matchid': str,
        # 'name': str,
        # 'nightstalker_night': bool,
        'paused': bool,
        # 'radiant_score': int,
        # 'ward_purchase_cooldown': int,
        'win_team': str
    },
    'player': {
        # 'accountid': str,
        'activity': str,
        # 'assists': int,
        # 'commands_issued': int,
        # 'deaths': int,
        # 'denies': int,
        # 'gold': int,
        'gold_from_creep_kills': int,
        'gold_from_hero_kills': int,
        'gold_from_income': int,
        'gold_from_shared': int,
        # 'gold_reliable': int,
        # 'gold_unreliable': int,
        'gpm': int,
        # 'kill_list': dict,
        'kill_streak': int,
        # 'kills': int,
        # 'last_hits': int,
        # 'name': str,
        # 'player_slot': int,
        # 'steamid': str,
        'team_name': str,
        # 'team_slot': int,
        'xpm': int
        },
    'provider': {
        # 'appid': int,
        # 'name': str,
        'timestamp': int,
        # 'version': int
        },
}

# Ключи gsi_data значения которых не требуются к сохранению в БД
# т.к. они не изменяются со временем или требуются лишь для первичной обработки
GSI_KEYS_FOR_DELETE = {
    'auth': None,
    'hero': ['name', ],
    'map': ['game_state', 'win_team', 'paused', 'matchid', ],
    'provider': None,
    'player': ['activity', 'team_name', ],
}

# Максимальное время в секундах прошедшее с последнего получения данных,
# после которого игра закрывается со статусом failed
TIME_FOR_GAME_FAIL = 600

# Максимальное время в секундах прошедшее с последнего получения данных,
# после которого, при закрытии игры, игрок закрывается со статусом failed
TIME_FOR_PLAYER_FAIL = 10
