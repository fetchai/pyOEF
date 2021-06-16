import fastapi

from services import agent_service

router = fastapi.APIRouter()


@router.get('/flush')
async def flush():
    await agent_service.redis_session.flush_redis()
    return {"status": "Db flushed."}
