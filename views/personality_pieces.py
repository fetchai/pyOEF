from starlette.requests import Request
import fastapi

from services import agent_service
from view_models.personality_pieces.genus_view_model import GenusViewModel
from view_models.register.acknowledge_view_model import AcknowledgeViewModel
from view_models.register.ping_view_model import PingViewModel
from view_models.register.register_view_model import RegisterViewModel
from view_models.register.set_position_view_model import SetPositionViewModel
from view_models.register.unregister_view_model import UnregisterViewModel

router = fastapi.APIRouter()


@router.post('/{unique_url}/set_genus')
async def set_genus(unique_url: str, request: Request):
    vm = GenusViewModel(unique_url, request)

    await vm.load()

    if vm.error:
        return {'error': vm.error}

    response = await agent_service.set_genus(agent_address=vm.agent_address,
                                             genus=vm.genus)
    return {"Respose": "Success"}
