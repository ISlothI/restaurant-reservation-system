from fastapi import HTTPException, status

from app.models.table import TableCreate, TableResponse, TableUpdate
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.slot_repository import SlotRepository
from app.repositories.table_repository import TableRepository


class TableService:
    @classmethod
    async def list_by_restaurant(cls, restaurant_id: str) -> list[TableResponse]:
        restaurant = await RestaurantRepository.find_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        docs = await TableRepository.find_by_restaurant(restaurant_id)
        return [cls._to_response(d) for d in docs]

    @classmethod
    async def get_by_id(cls, table_id: str) -> TableResponse:
        doc = await TableRepository.find_by_id(table_id)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        return cls._to_response(doc)

    @classmethod
    async def create(
        cls, restaurant_id: str, data: TableCreate, manager_id: str
    ) -> TableResponse:
        await cls._verify_ownership(restaurant_id, manager_id)
        doc = {
            "restaurant_id": restaurant_id,
            "name": data.name,
            "capacity": data.capacity,
            "table_type": data.table_type.value,
            "is_active": data.is_active,
        }
        created = await TableRepository.create(doc)
        return cls._to_response(created)

    @classmethod
    async def update(
        cls, restaurant_id: str, table_id: str, data: TableUpdate, manager_id: str
    ) -> TableResponse:
        await cls._verify_ownership(restaurant_id, manager_id)
        table = await TableRepository.find_by_id(table_id)
        if not table or table["restaurant_id"] != restaurant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")

        update_data = data.model_dump(exclude_none=True)
        if "table_type" in update_data and hasattr(update_data["table_type"], "value"):
            update_data["table_type"] = update_data["table_type"].value
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        updated = await TableRepository.update(table_id, update_data)
        return cls._to_response(updated)

    @classmethod
    async def delete(
        cls, restaurant_id: str, table_id: str, manager_id: str
    ) -> None:
        await cls._verify_ownership(restaurant_id, manager_id)
        table = await TableRepository.find_by_id(table_id)
        if not table or table["restaurant_id"] != restaurant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        slot_ids = await SlotRepository.find_ids_by_table(table_id)
        await ReservationRepository.cancel_by_slots(slot_ids)
        await SlotRepository.delete_by_table(table_id)
        await TableRepository.delete(table_id)

    @staticmethod
    async def _verify_ownership(restaurant_id: str, manager_id: str) -> dict:
        restaurant = await RestaurantRepository.find_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        if restaurant["manager_id"] != manager_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")
        return restaurant

    @staticmethod
    def _to_response(doc: dict) -> TableResponse:
        return TableResponse(
            id=doc["_id"],
            restaurant_id=doc["restaurant_id"],
            name=doc["name"],
            capacity=doc["capacity"],
            table_type=doc["table_type"],
            is_active=doc.get("is_active", True),
        )
