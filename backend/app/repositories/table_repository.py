from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database


class TableRepository:
    @staticmethod
    def _col(database: AsyncIOMotorDatabase | None = None):
        db = database or get_database()
        return db["tables"]

    @classmethod
    async def find_by_restaurant(cls, restaurant_id: str) -> list[dict]:
        cursor = cls._col().find({"restaurant_id": restaurant_id})
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @classmethod
    async def find_by_id(cls, table_id: str) -> dict | None:
        if not ObjectId.is_valid(table_id):
            return None
        doc = await cls._col().find_one({"_id": ObjectId(table_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @classmethod
    async def create(cls, data: dict) -> dict:
        result = await cls._col().insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    @classmethod
    async def update(cls, table_id: str, data: dict) -> dict | None:
        if not ObjectId.is_valid(table_id):
            return None
        await cls._col().update_one(
            {"_id": ObjectId(table_id)}, {"$set": data}
        )
        return await cls.find_by_id(table_id)

    @classmethod
    async def delete(cls, table_id: str) -> bool:
        if not ObjectId.is_valid(table_id):
            return False
        result = await cls._col().delete_one({"_id": ObjectId(table_id)})
        return result.deleted_count == 1

    @classmethod
    async def count_by_restaurant(cls, restaurant_id: str) -> int:
        return await cls._col().count_documents({"restaurant_id": restaurant_id})
