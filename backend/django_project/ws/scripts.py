from channels.layers import get_channel_layer

from django_project.scripts import get_redis_client


async def ws_group_send_message(group_name: str,
                                method_name: str,
                                message: dict = {}) -> None:
    """Send message to ws group if it exists."""
    key = f'asgi:group:{group_name}'
    channel_layer = get_channel_layer()
    r = get_redis_client()
    if r.exists(key):
        await channel_layer.group_send(
                group_name,
                {'type': method_name,
                 **message, },
                )
