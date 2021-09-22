import asyncio
import sys
from typing import Optional, List

import aredis
import redis
from aredis import StrictRedis

__async_client: Optional[aredis.StrictRedis] = None
__client: Optional[redis.client.Redis] = None


def global_init() -> None:
    global __client
    global __async_client
    try:
        __client = redis.Redis(host="localhost", port=6379, db=0, )
        __async_client = StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)


def create_sync_session() -> redis.client.Redis:
    global __client
    ping = __client.ping()

    if ping is True:
        return __client


async def flush_redis() -> None:
    await __async_client.flushdb()


async def create_async_session() -> aredis.client.StrictRedis:
    global __async_client
    ping = await __async_client.ping()
    if ping is True:
        return __async_client


async def get_table_name_by_classification(classification: str) -> List[str]:
    global __async_client
    keys: list = await __async_client.keys()
    accepted_keys = []
    for key in keys:
        if "fetch" not in key:
            if "*" == classification[0]:
                if classification[1:] in key:
                    accepted_keys.append(key)
            elif "*" == classification[-1]:
                if classification[:-2] in key:
                    accepted_keys.append(key)
            elif "*" not in classification:
                accepted_keys.append(classification)
    return accepted_keys
