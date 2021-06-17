from typing import Optional
from starlette.requests import Request

from services import agent_service
from view_models.shared.viewmodel import ViewModelBase

supported_genuses = [
    "Unclassified",  # Mark genus as *present*, but not set
    "Test",  # Agent is a *test* agent with no genus
    "Vehicle",  # A vehicle of some kind
    "Avatar",  # A representative of a person
    "Service",  # A service
    "IoT",  # Internet of Things device
    "Data",  # Attached to data source
    "Furniture",  # Sign, tree, etc.					(0.1.16)
    "Building",  # Large things						(0.1.18)
    "Buyer",  # A buyer only 					(0.1.19)
    "Viewer",  # Viewer, non-interactive agent 	(0.1.27) [e.g., OEF viewer app.]
    "Financial",  # DeFi agent						(0.2.8)
    "Thing",  # Representing a physical thing  	(0.3.10)
]


class GenusViewModel(ViewModelBase):
    def __init__(self, unique_url: str, request: Request):
        super().__init__(request)

        self.agent_address: Optional[str] = None
        self.soef_token: Optional[str] = None
        self.genus: Optional[str] = None
        self.unique_url: Optional[str] = unique_url

    async def load(self):

        request_data = await self.request.json()
        if not all(key in ["agent_address", "soef_token", "genus"] for key in request_data.keys()):
            self.error = (
                f"You need to provide the following parameters: ['agent_address', 'soef_token', 'genus'] "
            )
            return

        self.agent_address = request_data.get("agent_address")
        self.soef_token = request_data.get("soef_token")
        self.genus = request_data.get("genus")
        if not await agent_service.ensure_agent_is_acknowledged(
            self.agent_address, self.soef_token
        ):
            self.error = "You need to acknowledge the registration."
        elif not await agent_service.verify_unique_url(
            self.agent_address, self.unique_url
        ):
            self.error = "Your unique address is incorrect. Need to re-register."
        elif self.genus is None:
            self.error = f"You need to provide a genus.Choose one of {supported_genuses}"
        elif self.genus not in supported_genuses:
            self.error = (
                f"The genus is not supported. Choose one of {supported_genuses} "
            )
