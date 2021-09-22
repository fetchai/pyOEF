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

    async def load(self, method: str = 'post'):
        if method == 'get':
            request_data = self.request.query_params
        else:
            request_data = await self.request.json()
        self.soef_token = request_data.get("token")


        if await agent_service.get_agent_by_token(self.soef_token,  self.unique_url):
            self.error = "You already acknowledge or you need to register first."
