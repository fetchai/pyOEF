from typing import Optional
from urllib import parse
from starlette.requests import Request

from services import agent_service
from view_models.shared.viewmodel import ViewModelBase


class SetPositionViewModel(ViewModelBase):
    def __init__(self, unique_url: str, request: Request):
        super().__init__(request)

        self.agent_address: Optional[str] = None
        self.soef_token:  Optional[str] = None
        self.unique_url: Optional[str] = unique_url
        self.longitude: Optional[float] = None
        self.latitude: Optional[float] = None

    async def load(self):

        request_data = await self.request.json()
        self.agent_address = request_data.get("agent_address")
        self.soef_token = request_data.get("soef_token")
        self.latitude = float(request_data.get("latitude"))
        self.longitude = float(request_data.get("longitude"))

        if not await agent_service.ensure_agent_is_acknowledged(self.agent_address, self.soef_token):
            self.error = "You need to acknowledge the registration before you ping."
        elif not await agent_service.verify_unique_url(self.agent_address, self.unique_url):
            self.error = "Your unique address is incorrect. Need to re-register."
