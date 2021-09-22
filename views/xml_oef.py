from starlette.requests import Request
import fastapi
from starlette.responses import Response

from services import agent_service, search_service
from view_models.personality_pieces.personality_piece_view_model import PersonalityPieceViewModel
from view_models.personality_pieces.service_key_view_model import ServiceKeyViewModel
from view_models.register.acknowledge_view_model import AcknowledgeViewModel
from view_models.register.register_view_model import RegisterViewModel
from view_models.register.set_position_view_model import SetPositionViewModel
from xml_builders.xml_responses import generate_error_xml, registered_success_xml, command_success_xml

router = fastapi.APIRouter()


@router.get('/v1/register')
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


@router.get('/v1/{unique_url}')
async def get_commands(unique_url: str, request: Request):
    """Understand  the command and call the correct view model."""
    if request.query_params.get('command') == "acknowledge":
        vm = AcknowledgeViewModel(unique_url, request)
        await vm.load(method='get')

        if vm.error:
            xml_response = generate_error_xml(vm.error)
            return Response(content=xml_response, media_type="application/xml")

        await agent_service.create_verified_agent(vm.agent_address)
        return Response(content=command_success_xml(), media_type="application/xml")

    if request.query_params.get('command') == "set_position":
        vm = SetPositionViewModel(unique_url, request)
        await vm.load(method='get')

        if vm.error:
            xml_response = generate_error_xml(vm.error)
            return Response(content=xml_response, media_type="application/xml")
        await agent_service.set_position(unique_url=unique_url,
                                         latitude=vm.latitude,
                                         longitude=vm.longitude)
        return Response(content=command_success_xml(), media_type="application/xml")

    elif request.query_params.get('command') == "set_personality_piece":
        vm = PersonalityPieceViewModel(unique_url, request)
        await vm.load(method='get')

        if vm.error:
            xml_response = generate_error_xml(vm.error)
            return Response(content=xml_response, media_type="application/xml")

        if vm.piece == "genus":
            await agent_service.set_genus(unique_url=unique_url,
                                          genus=vm.value)
            await search_service.create_sets_based_on_genus(agent_address=vm.agent_address,
                                                            genus=vm.value)
        elif vm.piece == "classification":
            await agent_service.set_classification(unique_url=unique_url,
                                                   classification=vm.value)

            await search_service.create_sets_based_on_classification(agent_address=vm.agent_address,
                                                                     classification=vm.value)

        return Response(content=command_success_xml(), media_type="application/xml")

    elif request.query_params.get('command') == "set_service_key":
        vm = ServiceKeyViewModel(unique_url, request)
        await vm.load(method='get')

        await agent_service.set_service_keys(unique_url=unique_url,
                                             service_keys=vm.service_keys)

        if vm.error:
            xml_response = generate_error_xml(vm.error)
            return Response(content=xml_response, media_type="application/xml")

        return Response(content=command_success_xml(), media_type="application/xml")


