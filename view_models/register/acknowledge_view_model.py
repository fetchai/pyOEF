from typing import Optional

from starlette.requests import Request

from services import agent_service
from view_models.shared.viewmodel import ViewModelBase


class AcknowledgeViewModel(ViewModelBase):
    def __init__(self, unique_url: str, request: Request):
        super().__init__(request)

        self.agent_address: Optional[str] = None
        self.soef_token:  Optional[str] = None
        self.unique_url: Optional[str] = unique_url

    async def load(self):
        request_data = await self.request.json()
        self.agent_address = request_data.get("agent_address")
        self.soef_token = request_data.get("soef_token")
        if not await agent_service.get_agent_by_address(self.agent_address):
            self.error = "You already acknowledge or you need to register first."
        elif not await agent_service.verify_unique_url(self.agent_address, self.unique_url):
            self.error = "Your unique address is incorrect. Need to re-register."
