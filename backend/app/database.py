from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]


async def close_mongo_connection() -> None:
    global client
    if client:
        client.close()


def get_database() -> AsyncIOMotorDatabase:
    if db is None:
        raise RuntimeError("Database not initialised – call connect_to_mongo first")
    return db
