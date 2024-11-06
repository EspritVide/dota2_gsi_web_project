# Template for GSI cfg file
GAMESTATE_INTEGRATION_TEMPLATE = {
    "Gamestate Integration Script":
    {
        "uri": "http://127.0.0.1:8000/gsi/reciever/",
        "timeout": "5.0",
        "buffer": "1",
        "throttle": "1",
        "heartbeat": "10.0",
        "auth": {
            "token": None
        },
        "data": {
            "buildings": "1",
            "provider": "1",
            "map": "1",
            "player": "1",
            "hero": "1",
            "abilities": "1",
            "items": "1",
            "draft": "1",
            "wearables": "1"
        }
    }
}

# Path to GSI cfg file in local dota client
PATH_TO_CFG_FILE = 'game/dota/cfg/gamestate_integration/gamestate_integration_web.cfg'
