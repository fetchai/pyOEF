from typing import Optional
from starlette.requests import Request

from services import agent_service
from view_models.shared.viewmodel import ViewModelBase


class SetPositionViewModel(ViewModelBase):
    def __init__(self, unique_url: str, request: Request):
        super().__init__(request)

        self.agent_address: Optional[str] = None
        self.unique_url: Optional[str] = unique_url
        self.longitude: Optional[float] = None
        self.latitude: Optional[float] = None

    async def load(self, method: str = 'post'):

        if method == "get":
            request_data = self.request.query_params
        else:
            request_data = await self.request.json()

        if not all(key in ["agent_address", "latitude", "longitude"] for key in request_data.keys()):
            self.error = (
                f"You need to provide the following parameters: ['agent_address', 'soef_token', 'latitude', 'longitude'] "
            )
            return

        self.agent_address = request_data.get("agent_address")
        self.latitude = request_data.get("latitude")
        self.longitude = request_data.get("longitude")

        if not await agent_service.ensure_agent_is_verified(self.agent_address):
            self.error = "You need to acknowledge the registration before you ping."
        elif not await agent_service.verify_unique_url(self.agent_address, self.unique_url):
            self.error = "Your unique address is incorrect. Need to re-register."
        elif self.longitude is None or self.latitude is None:
            self.error = "You need to provide latitude and longitude."

