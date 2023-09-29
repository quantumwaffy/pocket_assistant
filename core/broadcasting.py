from broadcaster import Broadcast

from config import CONFIG


def get_broadcast() -> Broadcast:
    return Broadcast(CONFIG.REDIS.url)


broadcast: Broadcast = get_broadcast()
