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
import datetime
import uuid
from typing import Optional


class Agent:
    def __init__(self):
        """Initialise an agent."""
        self._agent_address: Optional[str] = None
        self._chain_identifier: Optional[str] = None
        self._declared_name: Optional[str] = None
        self._architecture: Optional[str] = None
        self._unique_token: Optional[str] = f"soef{str(uuid.uuid4())}"
        self._created_date: datetime.datetime = datetime.datetime.now()
        self._last_contacted: datetime.datetime = datetime.datetime.now()

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
    def unique_token(self) -> str:
        return self._unique_token

    @unique_token.setter
    def unique_token(self, value: str) -> None:
        self._unique_token = value

    @property
    def created_date(self) -> datetime.datetime:
        return self._created_date

    @property
    def last_contacted(self) -> datetime.datetime:
        return self._last_contacted
