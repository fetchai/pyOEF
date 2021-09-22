from typing import Optional
from starlette.requests import Request

from services import agent_service, search_service
from view_models.shared.viewmodel import ViewModelBase


class ClassificationViewModel(ViewModelBase):
    def __init__(self, unique_url: str, request: Request):
        super().__init__(request)

        self.agent_address: Optional[str] = None
        self.classification: Optional[str] = None
        self.unique_url: Optional[str] = unique_url

    async def load(self, method: str = 'post'):

        if method == 'get':
            request_data = self.request.query_params
        else:
            request_data = await self.request.json()

        if not all(key in ["agent_address", "classification"] for key in request_data.keys()):
            self.error = (
                f"You need to provide the following parameters: ['agent_address', 'soef_token', 'classification'] "
            )
            return

        self.agent_address = request_data.get("agent_address")
        self.soef_token = request_data.get("soef_token")
        self.classification = request_data.get("classification")
        # TODO: Validate that the classification does not contain special chars other  than `.`
        if not await agent_service.ensure_agent_is_acknowledged(
            self.agent_address, self.soef_token
        ):
            self.error = "You need to acknowledge the registration."
        elif not await agent_service.verify_unique_url(
            self.agent_address, self.unique_url
        ):
            self.error = "Your unique address is incorrect. Need to re-register."

        elif not search_service.special_match(self.classification):
            self.error = "Classification cannot contain any special character."

