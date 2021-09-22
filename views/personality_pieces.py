from starlette.requests import Request
import fastapi

from services import agent_service, search_service
from view_models.personality_pieces.classification_view_model import ClassificationViewModel
from view_models.personality_pieces.genus_view_model import GenusViewModel
from view_models.personality_pieces.service_key_view_model import ServiceKeyViewModel

router = fastapi.APIRouter()


@router.post('/{unique_url}/set_genus')
async def set_genus(unique_url: str, request: Request):
    vm = GenusViewModel(unique_url, request)

    await vm.load()

    if vm.error:
        return {'error': vm.error}

    response = await agent_service.set_genus(unique_url=unique_url,
                                             genus=vm.genus)

    await search_service.create_sets_based_on_genus(agent_address=vm.agent_address,
                                                    genus=vm.genus)
    return response


@router.post('/{unique_url}/set_classification')
async def set_classification(unique_url: str, request: Request):
    vm = ClassificationViewModel(unique_url, request)

    await vm.load()

    if vm.error:
        return {'error': vm.error}

    response = await agent_service.set_classification(unique_url=unique_url,
                                                      classification=vm.classification)

    await search_service.create_sets_based_on_classification(agent_address=vm.agent_address,
                                                             classification=vm.classification)
    return response


@router.post('/{unique_url}/set_service_key')
async def set_classification(unique_url: str, request: Request):
    vm = ServiceKeyViewModel(unique_url, request)

    await vm.load()

    if vm.error:
        return {'error': vm.error}

    response = await agent_service.set_service_keys(unique_url=unique_url,
                                                    service_keys=vm.service_keys)

    # TODO:// Store the service keys as tables ?

    return response
