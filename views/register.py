from starlette.requests import Request
import fastapi

from view_models.register.register_view_model import RegisterViewModel

router = fastapi.APIRouter()


@router.post('/register')
async def register(request: Request):
    vm = RegisterViewModel(request)
    await vm.load()

    if vm.error:
        return {'error': vm.error}

    # Create the account
    # account = await user_service.create_account(vm.name, vm.email, vm.password)
    #
    # # Login user
    # response = fastapi.responses.RedirectResponse(url='/account', status_code=status.HTTP_302_FOUND)
    # cookie_auth.set_auth(response, account.id)

    return {"Status": "Registered"}
