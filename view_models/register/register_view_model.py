import bech32
from typing import Optional
from eth_utils.address import is_address, is_checksum_address

from starlette.requests import Request

from services import agent_service
from view_models.shared.viewmodel import ViewModelBase

_FETCH = "fetch"

supported_chains = [
    "ethereum",
    "fetchai_cosmos",
    "fetchai_v1",
    "fetchai_v2_festnet_stable",
    "fetchai_v2_testnet_incentivised",
    "fetchai_v2_misc",
    "fetchai_v2_mainnet",
]

supported_architecture = ["Custom", "Framework"]


def is_valid_address(agent_address: str, chain_identifier: str) -> bool:
    if chain_identifier == "Ethereum":
        if not is_address(agent_address):
            return is_checksum_address(agent_address)
        return True
    elif chain_identifier in [
        "fetchai_cosmos",
        "fetchai_v1",
        "fetchai_v2_festnet_stable",
        "fetchai_v2_testnet_incentivised",
        "fetchai_v2_misc",
        "fetchai_v2_mainnet",
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

    async def load(self, method: str = "post"):
        if method == "get":
            request_data = self.request.query_params
        else:
            request_data = await self.request.json()
        self.declared_name = request_data.get("declared_name")
        self.agent_address = request_data.get("address")
        self.chain_identifier = request_data.get("chain_identifier")
        self.architecture = request_data.get("architecture")
        self.api_key = request_data.get('api_key')
        if self.chain_identifier.lower() not in supported_chains:
            self.error = "Chain identifier is not supported."
        elif not is_valid_address(self.agent_address, self.chain_identifier.lower()):
            self.error = "Agent address is not valid."
        elif self.api_key != "TwiCIriSl0mLahw17pyqoA":
            self.error = "Your api key is incorrect"
        elif await agent_service.get_agent_by_unique_url(self.agent_unique_address):
            self.error = "An agent with this address already exists."
