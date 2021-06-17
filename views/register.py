from starlette.requests import Request
import fastapi

from services import agent_service
from view_models.register.acknowledge_view_model import AcknowledgeViewModel
from view_models.register.ping_view_model import PingViewModel
from view_models.register.register_view_model import RegisterViewModel

router = fastapi.APIRouter()


@router.post('/register')
async def register(request: Request):
    vm = RegisterViewModel(request)
    await vm.load()

    if vm.error:
        return {'error': vm.error}

    # Create the agent.
    unique_url, soef_token = await agent_service.create_agent_to_lobby(agent_address=vm.agent_address,
                                                                       chain_identifier=vm.chain_identifier,
                                                                       declared_name=vm.declared_name,
                                                                       architecture=vm.architecture)
    response = {
        "status": "lobby",
        "unique_url": unique_url,
        "soef_token": soef_token
    }

    return response


@router.post('/{unique_url}/acknowledge')
async def acknowledge(unique_url: str, request: Request):
    vm = AcknowledgeViewModel(unique_url, request)
    await vm.load()

    if vm.error:
        return {'error': vm.error}

    agent = await agent_service.create_verified_agent(vm.agent_address)

    return agent.__dict__


@router.get('/{unique_url}/ping')
async def ping(unique_url: str, request: Request):
    vm = PingViewModel(unique_url, request)

    await vm.load()

    if vm.error:
        return {'error': vm.error}
