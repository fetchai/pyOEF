from starlette.requests import Request
import fastapi

from data import redis_session
from services import agent_service, search_service
from view_models.register.acknowledge_view_model import AcknowledgeViewModel
from view_models.register.ping_view_model import PingViewModel
from view_models.register.register_view_model import RegisterViewModel
from view_models.register.set_position_view_model import SetPositionViewModel
from view_models.register.unregister_view_model import UnregisterViewModel
from view_models.search.search_around_me_view_model import SearchAroundMeViewModel

router = fastapi.APIRouter()


@router.post('/search_around_me')
async def search(request: Request):
    vm = SearchAroundMeViewModel(request)
    await vm.load()
    agents = await search_service.find_around_me(vm.radius, vm.latitude,  vm.latitude)
    return {"agents": agents}