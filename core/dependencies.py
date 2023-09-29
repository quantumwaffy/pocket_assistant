from typing import Annotated

from fastapi import Depends
from motor import motor_asyncio

from config import CONFIG


async def get_no_sql_client() -> motor_asyncio.AsyncIOMotorDatabase:
    client: motor_asyncio.AsyncIOMotorClient = CONFIG.MONGO.client
    try:
        yield client[CONFIG.MONGO.MONGO_INITDB_DATABASE]
    finally:
        client.close()


NoSqlSession = Annotated[motor_asyncio.AsyncIOMotorDatabase, Depends(get_no_sql_client)]
