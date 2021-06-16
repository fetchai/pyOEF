import bech32
from typing import Optional
from eth_utils.address import is_address, is_checksum_address

from starlette.requests import Request

from services import agent_service
from view_models.shared.viewmodel import ViewModelBase

_FETCH = "fetch"

supported_chains = [
    "Ethereum",
    "Fetchai_cosmos",
    "FetchAI_v1",
    "FetchAI_v2_Testnet_Stable",
    "FetchAI_v2_Testnet_Incentivised",
    "FetchAI_v2_Misc",
    "FetchAI_v2_Mainnet",
]

supported_architecture = ["Custom", "Framework"]


def is_valid_address(agent_address: str, chain_identifier: str) -> bool:
    if chain_identifier == "Ethereum":
        if not is_address(agent_address):
            return is_checksum_address(agent_address)
        return True
    elif chain_identifier in [
        "Fetchai_cosmos",
        "FetchAI_v1",
        "FetchAI_v2_Testnet_Stable",
        "FetchAI_v2_Testnet_Incentivised",
        "FetchAI_v2_Misc",
        "FetchAI_v2_Mainnet",
    ]:
        result = bech32.bech32_decode(agent_address)
        return result != (None, None) and result[0] == _FETCH


class RegisterViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.agent_address: Optional[str] = None
        self.chain_identifier: Optional[str] = None
        self.declared_name: Optional[str] = None
        self.architecture: Optional[str] = None
        self.api_key: Optional[str] = None

    async def load(self):
        request_data = await self.request.json()
        self.declared_name = request_data.get("declared_name")
        self.agent_address = request_data.get("agent_address")
        self.chain_identifier = request_data.get("chain_identifier")
        self.architecture = request_data.get("architecture")
        self.api_key = request_data.get('api_key')
        if self.chain_identifier not in supported_chains:
            self.error = "Chain identifier is not supported."
        elif not is_valid_address(self.agent_address, self.chain_identifier):
            self.error = "Agent address is not valid."
        elif self.api_key != "TwiCIriSl0mLahw17pyqoA":
            self.error = "Your api key is incorrect"
        elif self.architecture.capitalize() not in supported_architecture:
            self.error = "Architecture is not supported."
        elif await agent_service.get_agent_by_address(self.agent_address):
            self.error = "An agent with this address already exists."
