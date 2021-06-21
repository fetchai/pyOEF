import random

import requests
from aea.crypto.wallet import Wallet
from aea_ledger_fetchai import FetchAICrypto
from aea.crypto.helpers import create_private_key

url = "http://127.0.0.1:8000/"
for i in range(1, 100):
    create_private_key(FetchAICrypto.identifier, private_key_file='private_key.txt')
    wallet_1 = Wallet({FetchAICrypto.identifier: 'private_key.txt'})
    params = {
        "declared_name": f"agent_test_{i}",
        "agent_address": wallet_1.addresses.get(FetchAICrypto.identifier),
        "chain_identifier": "FetchAI_v2_Testnet_Stable",
        "architecture": "custom",
        "api_key": "TwiCIriSl0mLahw17pyqoA"
    }
    path = url + "register"
    register_request = requests.post(url=path, json=params)
    response_dict = register_request.json()
    if response_dict.get('status_code') == 200:
        params = {
                "agent_address": wallet_1.addresses.get(FetchAICrypto.identifier),
                "soef_token": response_dict.get("soef_token")
        }
        path = url + f"{response_dict.get('unique_url')}/acknowledge"
        acknowledge_request = requests.post(url=path, json=params)
        acknowledge_dict = acknowledge_request.json()
        if acknowledge_dict.get('status_code') == 200:
            path = url + f"{response_dict.get('unique_url')}/set_position"
            params = {
                "agent_address": wallet_1.addresses.get(FetchAICrypto.identifier),
                "soef_token": response_dict.get('soef_token'),
                "latitude": 52.205278 + ((random.random() * 2.0) - 1.0),
                "longitude": 0.11 + ((random.random() * 2.0) - 1.0)
            }
            set_pos_request = requests.post(url=path, json=params)
            print(set_pos_request.json())