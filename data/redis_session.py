import asyncio
import sys
from typing import Optional

import aredis
import redis
from aredis import StrictRedis

__async_client: Optional[aredis.StrictRedis] = None
__client : Optional[redis.client.Redis] = None


def global_init() -> None:
    global __client
    global __async_client
    try:
        __client = redis.Redis(host="localhost", port=6379, db=0, )
        __async_client = StrictRedis(host='127.0.0.1', port=6379, db=0)
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)


def create_sync_session() -> redis.client.Redis:
    global __client
    ping = __client.ping()

    if ping is True:
        return __client


async def create_async_session() -> aredis.client.StrictRedis:
    global __async_client
    ping = await __async_client.ping()
    if ping is True:
        return __async_client







