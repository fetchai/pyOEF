import random

import requests
from aea.crypto.wallet import Wallet
from aea_ledger_fetchai import FetchAICrypto
from aea.crypto.helpers import create_private_key

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

classification_list = [
    "test.hotel.client",
    "test.hotel.service",
    "test.ddn.driver",
    "test.ddn.client",
    "test.mobility.train",
    "test.mobility.station",
    "test.fault.service",
    "test.fault.agent",
    "test.supply.machine",
    "test.supply.company",
]

url = "http://127.0.0.1:8000/"
for i in range(1, 500):
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
            # Set Position.
            path = url + f"{response_dict.get('unique_url')}/set_position"
            params = {
                "agent_address": wallet_1.addresses.get(FetchAICrypto.identifier),
                "soef_token": response_dict.get('soef_token'),
                "latitude": 52.205278 + ((random.random() * 2.0) - 1.0),
                "longitude": 0.11 + ((random.random() * 2.0) - 1.0)
            }
            set_pos_request = requests.post(url=path, json=params)

            # Set Genus

            path = url + f"{response_dict.get('unique_url')}/set_genus"
            params = {
                "agent_address": wallet_1.addresses.get(FetchAICrypto.identifier),
                "soef_token": response_dict.get('soef_token'),
                "genus": supported_genuses[random.randint(1, len(supported_genuses) - 1)]
            }
            set_genus_request = requests.post(url=path, json=params)

            # Set Classification:

            path = url + f"{response_dict.get('unique_url')}/set_classification"
            params = {
                "agent_address": wallet_1.addresses.get(FetchAICrypto.identifier),
                "soef_token": response_dict.get('soef_token'),
                "classification": classification_list[random.randint(1, len(classification_list) - 1)]
            }
            set_classification_request = requests.post(url=path, json=params)

