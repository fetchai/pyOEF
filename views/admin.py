import time

import fastapi
from fastapi_utils.tasks import repeat_every
from services import agent_service
from data import redis_session

router = fastapi.APIRouter()


@router.get('/flush')
async def flush():
    await redis_session.flush_redis()
    return {"status": "Db flushed."}


@router.get('/keys')
async def keys():
    client = await redis_session.create_async_session()
    keys: list = await client.keys()
    accepted_keys = []
    key_members  = {}
    for key in keys:
        if "fetch" not in key:
            accepted_keys.append(key)
            members = await client.smembers(key)
            key_members.update({key: len(members)})
    return {**key_members, "keys": accepted_keys}


@router.on_event("startup")
@repeat_every(seconds=900)
async def clean_up():
    client = await redis_session.create_async_session()
    lobby = [address for address in await client.smembers('lobby')]
    verified_agents = [address for address in await client.smembers('agents')]
    agents = lobby + verified_agents
    for address in agents:
        table = ''
        agent_dict = await client.hgetall(address)
        timeout_time = int(time.time()) - int(agent_dict.get('_last_contacted'))
        if timeout_time > 3600:
            await client.srem(agent_dict.get('_status'), address)
            await client.delete(address)
            classification_list = agent_dict.get('_classification').split('.')
            for item in classification_list:
                table += "." + item
                await client.sismember(table[1:], address)

        else:
            print(timeout_time)


