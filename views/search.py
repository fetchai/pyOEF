from starlette.requests import Request
import fastapi

from services import search_service
from view_models.search.find_around_me_view_model import FindAroundMeViewModel

router = fastapi.APIRouter()


@router.post('/find_around_me')
async def search(request: Request):
    vm = FindAroundMeViewModel(request)
    await vm.load()
    if vm.error:
        return {'error': vm.error}
    agents = await search_service.find_around_me(vm.radius, vm.latitude,  vm.latitude)
    return {
        "status_code": 200,
        "agents": agents
    }