# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2020-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
import time
import uuid
from typing import Optional, Dict


class Agent:
    def __init__(self):
        """Initialise an agent."""
        self._agent_address: Optional[str] = None
        self._chain_identifier: Optional[str] = None
        self._declared_name: Optional[str] = None
        self._architecture: Optional[str] = None
        self._status: Optional[str] = None
        self._latitude: Optional[float] = None
        self._longitude: Optional[float] = None
        self._genus: Optional[str] = None
        self._unique_url: Optional[str] = f"soef_{str(uuid.uuid4())}"
        self._soef_token: Optional[str] = f"token_{str(uuid.uuid4())}"
        self._created_date: int = int(time.time())
        self._last_contacted: int = int(time.time())

    @property
    def agent_address(self) -> str:
        return self._agent_address

    @agent_address.setter
    def agent_address(self, value: str) -> None:
        self._agent_address = value

    @property
    def chain_identifier(self) -> str:
        return self._chain_identifier

    @chain_identifier.setter
    def chain_identifier(self, value: str) -> None:
        self._chain_identifier = value

    @property
    def declared_name(self) -> str:
        return self._declared_name

    @declared_name.setter
    def declared_name(self, value: str) -> None:
        self._declared_name = value

    @property
    def architecture(self) -> str:
        return self._architecture

    @architecture.setter
    def architecture(self, value) -> None:
        self._architecture = value

    @property
    def soef_token(self) -> str:
        return self._soef_token

    @property
    def unique_url(self) -> str:
        return self._unique_url

    @property
    def created_date(self) -> int:
        return self._created_date

    @property
    def last_contacted(self) -> int:
        return self._last_contacted

    @last_contacted.setter
    def last_contacted(self, value) -> None:
        self._last_contacted = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value) -> None:
        self._status = value

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value) -> None:
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value) -> None:
        self._longitude = value

    @property
    def genus(self) -> str:
        return self._genus

    @genus.setter
    def genus(self, value) -> None:
        self._genus = value

    @classmethod
    def from_dict(cls, agent_dict: Dict[str, str]):
        agent = cls()
        agent._agent_address = agent_dict.get("_agent_address")
        agent._chain_identifier = agent_dict.get("_chain_identifier")
        agent._declared_name = agent_dict.get('_declared_name')
        agent._architecture = agent_dict.get('_architecture')
        agent._unique_url = agent_dict.get('_unique_url')
        agent._soef_token = agent_dict.get('_soef_token')
        agent._created_date = agent_dict.get('_created_date')
        agent._last_contacted = agent_dict.get('_last_contacted')
        agent._status = agent_dict.get('_status')
        agent._latitude = agent_dict.get('_latitude')
        agent._longitude = agent_dict.get('_longitude')
        agent._genus = agent_dict.get('_genus')

        return agent


