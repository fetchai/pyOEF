from typing import Optional
from starlette.requests import Request

from services import agent_service, search_service
from view_models.personality_pieces.genus_view_model import supported_genuses
from view_models.shared.viewmodel import ViewModelBase


class PersonalityPieceViewModel(ViewModelBase):
    def __init__(self, unique_url: str, request: Request):
        super().__init__(request)

        self.agent_address: Optional[str] = None
        self.piece: Optional[str] = None
        self.value: Optional[str] = None
        self.unique_url: Optional[str] = unique_url

    async def load(self, method: str = 'post'):

        if method == 'get':
            request_data = self.request.query_params
        else:
            request_data = await self.request.json()

        if not all(key in ["agent_address", "piece", "value"] for key in request_data.keys()):
            self.error = (
                f"You need to provide the following parameters: ['agent_address', 'piece', 'value'] "
            )
            return

        self.agent_address = request_data.get("agent_address")
        self.piece = request_data.get("piece")
        self.value = request_data.get("value")
        # TODO: Validate that the classification does not contain special chars other  than `.`
        if not await agent_service.ensure_agent_is_verified(
            self.agent_address
        ):
            self.error = "You need to acknowledge the registration."
        elif self.value is None:
            self.error = f"You need to provide a value for {self.piece}"
            return

        if self.piece == 'classification':
            if not search_service.special_match(self.value):
                self.error = "Classification cannot contain any special character."
        elif self.piece == 'genus':
            if self.value not in supported_genuses:
                self.error = (
                    f"The genus is not supported. Choose one of {supported_genuses} "
                )

