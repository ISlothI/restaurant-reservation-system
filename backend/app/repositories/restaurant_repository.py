from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database


class RestaurantRepository:
    @staticmethod
    def _col(database: AsyncIOMotorDatabase | None = None):
        db = database or get_database()
        return db["restaurants"]

    @classmethod
    async def find_all(cls, filters: dict | None = None) -> list[dict]:
        query = filters or {}
        cursor = cls._col().find(query)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @classmethod
    async def find_by_id(cls, restaurant_id: str) -> dict | None:
        if not ObjectId.is_valid(restaurant_id):
            return None
        doc = await cls._col().find_one({"_id": ObjectId(restaurant_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @classmethod
    async def find_by_manager(cls, manager_id: str) -> dict | None:
        doc = await cls._col().find_one({"manager_id": manager_id})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @classmethod
    async def create(cls, data: dict) -> dict:
        result = await cls._col().insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    @classmethod
    async def update(cls, restaurant_id: str, data: dict) -> dict | None:
        if not ObjectId.is_valid(restaurant_id):
            return None
        await cls._col().update_one(
            {"_id": ObjectId(restaurant_id)}, {"$set": data}
        )
        return await cls.find_by_id(restaurant_id)

    @classmethod
    async def delete(cls, restaurant_id: str) -> bool:
        if not ObjectId.is_valid(restaurant_id):
            return False
        result = await cls._col().delete_one({"_id": ObjectId(restaurant_id)})
        return result.deleted_count == 1

    @classmethod
    async def count(cls) -> int:
        return await cls._col().count_documents({})
