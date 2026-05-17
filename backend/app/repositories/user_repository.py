from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database


class UserRepository:
    @staticmethod
    def _col(database: AsyncIOMotorDatabase | None = None):
        db = database or get_database()
        return db["users"]

    @classmethod
    async def find_by_email(cls, email: str) -> dict | None:
        return await cls._col().find_one({"email": email})

    @classmethod
    async def find_by_id(cls, user_id: str) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        doc = await cls._col().find_one({"_id": ObjectId(user_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @classmethod
    async def create(cls, user_data: dict) -> dict:
        result = await cls._col().insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return user_data

    @classmethod
    async def update(cls, user_id: str, data: dict) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        await cls._col().update_one(
            {"_id": ObjectId(user_id)}, {"$set": data}
        )
        return await cls.find_by_id(user_id)

    @classmethod
    async def count(cls) -> int:
        return await cls._col().count_documents({})
