import math
import re

from data import redis_session


async def create_sets_based_on_classification(agent_address: str, classification: str) -> None:
    client = await redis_session.create_async_session()
    classification_list = classification.split('.')
    table = ""
    for item in classification_list:
        table += "."+item
        await client.sadd(table[1:], agent_address)


async def create_sets_based_on_genus(agent_address:str, genus: str) -> None:
    client = await redis_session.create_async_session()
    await client.sadd(genus, agent_address)


def special_match(strg, search=re.compile(r'[^a-z.]').search):
    return not bool(search(strg))


async def find_around_me(radius: float, latitude: float, longitude: float, genus: str = None, classification: str = None):
    client = await redis_session.create_async_session()
    entries = await client.smembers('v_agents')
    agents = []
    for address in entries:
        agent = await client.hgetall(address)
        calculate_distance = abs(math.sqrt((latitude - float(agent.get('_latitude'))) ** 2 + (longitude - float(agent.get('_longitude'))) ** 2) - radius)
        if calculate_distance < radius:
            agents.append(address)
    return agents
