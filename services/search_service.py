import math
import re
from typing import List

from data import redis_session


async def create_sets_based_on_classification(
    agent_address: str, classification: str
) -> None:
    client = await redis_session.create_async_session()
    classification_list = classification.split(".")
    table = ""
    for item in classification_list:
        table += "." + item
        await client.sadd(table[1:], agent_address)


async def create_sets_based_on_genus(agent_address: str, genus: str) -> None:
    client = await redis_session.create_async_session()
    await client.sadd(genus, agent_address)


def special_match(strg, search=re.compile(r"[^a-z.]").search):
    return not bool(search(strg))


async def find_around_me(
    radius: float,
    latitude: float,
    longitude: float,
    genus: str = None,
    classification: str = None,
) -> List[str]:
    client = await redis_session.create_async_session()
    members = await find_members(genus, classification)
    agents = []
    for address in members:
        agent = await client.hgetall(address)
        calculate_distance = abs(
            math.sqrt(
                (latitude - float(agent.get("_latitude"))) ** 2
                + (longitude - float(agent.get("_longitude"))) ** 2
            )
            - radius
        )
        if calculate_distance < radius:
            agents.append(address)
    return agents


async def find_members(genus: str, classification: str):
    client = await redis_session.create_async_session()
    members = None
    if genus is not None:
        members = await client.smembers("genus")
    if classification is not None:
        redis_tables = await redis_session.get_table_name_by_classification(
            classification
        )
        if members is None:
            for key in redis_tables:
                members += await client.smembers(key)
        elif members is not None:
            for key in redis_tables:
                returned_members = await client.smembers(key)
                for item in members:
                    if item not in returned_members:
                        members.remove(item)
    if genus is None and classification is None:
        members = await client.smembers("v_agents")

    return members
