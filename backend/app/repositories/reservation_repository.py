from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database


class ReservationRepository:
    @staticmethod
    def _col(database: AsyncIOMotorDatabase | None = None):
        db = database or get_database()
        return db["reservations"]

    @classmethod
    async def find_by_user(cls, user_id: str, status: str | None = None) -> list[dict]:
        query: dict = {"user_id": user_id}
        if status:
            query["status"] = status
        cursor = cls._col().find(query).sort("created_at", -1)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @classmethod
    async def find_by_restaurant(
        cls, restaurant_id: str, status: str | None = None
    ) -> list[dict]:
        query: dict = {"restaurant_id": restaurant_id}
        if status:
            query["status"] = status
        cursor = cls._col().find(query).sort("created_at", -1)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @classmethod
    async def find_by_id(cls, reservation_id: str) -> dict | None:
        if not ObjectId.is_valid(reservation_id):
            return None
        doc = await cls._col().find_one({"_id": ObjectId(reservation_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @classmethod
    async def find_by_slot(cls, slot_id: str) -> list[dict]:
        cursor = cls._col().find({"slot_id": slot_id, "status": {"$ne": "cancelled"}})
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @classmethod
    async def create(cls, data: dict) -> dict:
        result = await cls._col().insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    @classmethod
    async def update(cls, reservation_id: str, data: dict) -> dict | None:
        if not ObjectId.is_valid(reservation_id):
            return None
        await cls._col().update_one(
            {"_id": ObjectId(reservation_id)}, {"$set": data}
        )
        return await cls.find_by_id(reservation_id)

    @classmethod
    async def delete(cls, reservation_id: str) -> bool:
        if not ObjectId.is_valid(reservation_id):
            return False
        result = await cls._col().delete_one({"_id": ObjectId(reservation_id)})
        return result.deleted_count == 1

    @classmethod
    async def count_active_by_slot(cls, slot_id: str) -> int:
        return await cls._col().count_documents(
            {"slot_id": slot_id, "status": {"$ne": "cancelled"}}
        )

    @classmethod
    async def cancel_by_slot(cls, slot_id: str) -> int:
        result = await cls._col().update_many(
            {"slot_id": slot_id, "status": {"$ne": "cancelled"}},
            {"$set": {"status": "cancelled"}},
        )
        return result.modified_count

    @classmethod
    async def cancel_by_slots(cls, slot_ids: list[str]) -> int:
        if not slot_ids:
            return 0
        result = await cls._col().update_many(
            {"slot_id": {"$in": slot_ids}, "status": {"$ne": "cancelled"}},
            {"$set": {"status": "cancelled"}},
        )
        return result.modified_count
