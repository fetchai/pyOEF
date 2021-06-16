# from typing import Optional
#
#
# from data.agent import Agent
# from data import db_session
import json

from data import redis_session
from data.agent import Agent


async def get_user_by_address(agent_address: str) -> bool:
    pass


async def create_agent_to_lobby(agent_address: str, chain_identifier: str, declared_name: str, architecture: str) -> str:
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

    return agent.unique_token, agent.unique_url


# async def create_account(name: str, email: str, password: str) -> User:
#     user = User()
#     user.name = name
#     user.email = email
#     # TODO: set proper password
#     user.hash_password = crypto.hash(password, rounds=172_434)
#
#     async with db_session.create_async_session() as session:
#         session.add(user)
#         await session.commit()
#
#     return user
#
#
# async def login_user(email: str, password: str) -> Optional[User]:
#     async with db_session.create_async_session() as session:
#         query = select(User).filter(User.email == email)
#         results = await session.execute(query)
#         user = results.scalar_one_or_none()
#         if not user:
#             return user
#         if not crypto.verify(password, user.hash_password):
#             return None
#         return user
#
#
# async def get_user_by_id(user_id: int) -> Optional[User]:
#     async with db_session.create_async_session() as session:
#         query = select(User).filter(User.id == user_id)
#         result = await session.execute(query)
#
#         return result.scalar_one_or_none()
#
#
# async def get_user_by_email(email: str) -> Optional[User]:
#     async with db_session.create_async_session() as session:
#         query = select(User).filter(User.email == email)
#         result = await session.execute(query)
#
#         return result.scalar_one_or_none()