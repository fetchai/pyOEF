from starlette.requests import Request
import fastapi
from starlette.responses import Response

from services import agent_service
from view_models.register.register_view_model import RegisterViewModel
from xml_builders.xml_responses import generate_error_xml, registered_success_xml

router = fastapi.APIRouter()


@router.get('/register')
async def get_register(request: Request):
    """Register request. Method: GET"""
    vm = RegisterViewModel(request)
    await vm.load(method=request.method.lower())

    if vm.error:
        xml_response = generate_error_xml(vm.error)
        return Response(content=xml_response, media_type="application/xml")

    # Create the agent.
    unique_url, soef_token = await agent_service.create_agent_to_lobby(agent_address=vm.agent_address,
                                                                       chain_identifier=vm.chain_identifier,
                                                                       declared_name=vm.declared_name,
                                                                       )
    xml_response = registered_success_xml(unique_url, soef_token)
    return Response(content=xml_response, media_type="application/xml")


@router.get('/{unique_url}')
async def get_commands(unique_url: str, request: Request):
    """Understand  the command and call the correct view model."""
