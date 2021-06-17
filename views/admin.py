import time

import fastapi
from fastapi_utils.tasks import repeat_every
from services import agent_service
from data import redis_session

router = fastapi.APIRouter()


@router.get('/flush')
async def flush():
    await agent_service.redis_session.flush_redis()
    return {"status": "Db flushed."}


@router.on_event("startup")
@repeat_every(seconds=900)
async def clean_up():
    client = await redis_session.create_async_session()
    lobby = [address for address in await client.smembers('lobby')]
    verified_agents = [address for address in await client.smembers('agents')]
    agents = lobby + verified_agents
    for address in agents:
        agent_dict = await client.hgetall(address)
        timeout_time = int(time.time()) - int(agent_dict.get('_last_contacted'))
        if timeout_time > 3600:
            await client.srem(agent_dict.get('_status'), address)
            await client.delete(address)

        else:
            print(timeout_time)

