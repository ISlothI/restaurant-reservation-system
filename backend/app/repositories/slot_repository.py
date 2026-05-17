from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database


class SlotRepository:
    @staticmethod
    def _col(database: AsyncIOMotorDatabase | None = None):
        db = database or get_database()
        return db["reservation_slots"]

    @classmethod
    async def find_by_restaurant(
        cls, restaurant_id: str, status: str | None = None
    ) -> list[dict]:
        query: dict = {"restaurant_id": restaurant_id}
        if status:
            query["status"] = status
        cursor = cls._col().find(query)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @classmethod
    async def find_by_id(cls, slot_id: str) -> dict | None:
        if not ObjectId.is_valid(slot_id):
            return None
        doc = await cls._col().find_one({"_id": ObjectId(slot_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @classmethod
    async def create(cls, data: dict) -> dict:
        result = await cls._col().insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    @classmethod
    async def update(cls, slot_id: str, data: dict) -> dict | None:
        if not ObjectId.is_valid(slot_id):
            return None
        await cls._col().update_one(
            {"_id": ObjectId(slot_id)}, {"$set": data}
        )
        return await cls.find_by_id(slot_id)

    @classmethod
    async def delete(cls, slot_id: str) -> bool:
        if not ObjectId.is_valid(slot_id):
            return False
        result = await cls._col().delete_one({"_id": ObjectId(slot_id)})
        return result.deleted_count == 1

    @classmethod
    async def find_ids_by_table(cls, table_id: str) -> list[str]:
        cursor = cls._col().find({"table_id": table_id}, {"_id": 1})
        return [str(doc["_id"]) async for doc in cursor]

    @classmethod
    async def delete_by_table(cls, table_id: str) -> int:
        result = await cls._col().delete_many({"table_id": table_id})
        return result.deleted_count

    @classmethod
    async def count_by_restaurant(cls, restaurant_id: str) -> int:
        return await cls._col().count_documents({"restaurant_id": restaurant_id})
