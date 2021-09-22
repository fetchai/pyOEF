from starlette.requests import Request
import fastapi
from starlette.responses import Response

from services import agent_service
from view_models.register.register_view_model import RegisterViewModel
from xml_builders.xml_responses import generate_error_xml, registered_success_xml

router = fastapi.APIRouter()


@router.get('/{request_path}')
async def get_request_command(request_path, request: Request):
    # TODO: At this point we will process the request and identify the command. based
    # TODO: on the command we will call the correct view model and then create the xml response.
    if request_path == "register":
        return await register_vm(request)


async def register_vm(request: Request):
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