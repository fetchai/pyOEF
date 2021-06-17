import time

from data import redis_session
from data.agent import Agent


async def get_agent_by_address(agent_address: str) -> bool:
    client = await redis_session.create_async_session()
    agent = await client.sismember('lobby', agent_address)
    return agent


async def ensure_agent_is_acknowledged(agent_address: str, soef_token: str) -> bool:
    client = await redis_session.create_async_session()
    agent_dict = await client.hgetall(agent_address)
    return await client.sismember('v_agents', agent_address) and agent_dict.get("_soef_token") == soef_token


async def verify_unique_url(agent_address: str, unique_url: str):
    client = await redis_session.create_async_session()
    agent = await client.hgetall(agent_address)
    return agent.get("_unique_url") == unique_url


async def create_agent_to_lobby(agent_address: str, chain_identifier: str, declared_name: str, architecture: str):
    agent = Agent()
    agent.agent_address = agent_address
    agent.chain_identifier = chain_identifier
    agent.declared_name = declared_name
    agent.architecture = architecture
    agent.status = "lobby"
    client = await redis_session.create_async_session()

    # Adding the agent to the  lobby.
    await client.sadd("lobby", agent.agent_address)
    # Storing the values of the agent in a hash table.
    await client.hmset(agent.agent_address, agent.__dict__)

    return agent.unique_url, agent.soef_token


async def create_verified_agent(agent_address: str) -> Agent:
    client = await redis_session.create_async_session()
    agent_dict = await client.hgetall(agent_address)
    agent = Agent.from_dict(agent_dict)
    agent._status = "v_agents"
    agent._last_contacted = int(time.time())
    await client.hmset(agent.agent_address, agent.__dict__)
    await client.smove("lobby", "v_agents", agent.agent_address)
    print(await client.smembers("v_agents"))
    print(await client.smembers("lobby"))
    return agent
