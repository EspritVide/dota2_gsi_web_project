import redis

from .settings import CHANNEL_LAYERS


def get_redis_client():
    return redis.Redis(
        *CHANNEL_LAYERS['default']['CONFIG']['hosts'][0],
        decode_responses=True)
