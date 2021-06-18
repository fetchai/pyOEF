import re

from data import redis_session


async def create_sets_based_on_classification(agent_address: str, classification: str) -> None:
    client = await redis_session.create_async_session()
    classification_list = classification.split('.')
    table = ""
    for item in classification_list:
        table += "."+item
        await client.sismember(table[1:], agent_address)


def special_match(strg, search=re.compile(r'[^a-z.]').search):
    return not bool(search(strg))
