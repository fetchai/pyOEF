from starlette.requests import Request
import fastapi

router = fastapi.APIRouter()


#### THIS IS THE XML SUPPORT TO MIMIC THE EXISTING SOEF  ####

@router.get('/{unique_url/')
async def get_request_command(unique_url: str, request: Request):
    # TODO: At this point we will process the request and identify the command. based
    # TODO: on the command we will call the correct view model and then create the xml response.
    pass