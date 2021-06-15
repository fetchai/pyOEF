from typing import Optional, Dict

from starlette.requests import Request


class ViewModelBase:

    def __init__(self, request: Request):

        self.request: Request = request
        self.error: Optional[str] = None
        self.agent_unique_address: Optional[str] = None

    def to_dict(self) -> Dict:
        return self.__dict__
