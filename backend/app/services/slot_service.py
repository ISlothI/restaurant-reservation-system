from fastapi import HTTPException, status

from app.models.reservation_slot import (
    ReservationSlotCreate,
    ReservationSlotResponse,
    ReservationSlotUpdate,
)
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.slot_repository import SlotRepository
from app.repositories.table_repository import TableRepository


class SlotService:
    @classmethod
    async def list_by_restaurant(
        cls, restaurant_id: str, slot_status: str | None = None
    ) -> list[ReservationSlotResponse]:
        restaurant = await RestaurantRepository.find_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        docs = await SlotRepository.find_by_restaurant(restaurant_id, status=slot_status)
        return [cls._to_response(d) for d in docs]

    @classmethod
    async def get_by_id(cls, slot_id: str) -> ReservationSlotResponse:
        doc = await SlotRepository.find_by_id(slot_id)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
        return cls._to_response(doc)

    @classmethod
    async def create(
        cls, restaurant_id: str, data: ReservationSlotCreate, manager_id: str
    ) -> ReservationSlotResponse:
        await cls._verify_ownership(restaurant_id, manager_id)

        table = await TableRepository.find_by_id(data.table_id)
        if not table or table["restaurant_id"] != restaurant_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Table not found in this restaurant")

        if data.start_at >= data.end_at:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="start_at must be before end_at")

        doc = {
            "restaurant_id": restaurant_id,
            "table_id": data.table_id,
            "start_at": data.start_at,
            "end_at": data.end_at,
            "status": data.status.value,
        }
        created = await SlotRepository.create(doc)
        return cls._to_response(created)

    @classmethod
    async def update(
        cls, restaurant_id: str, slot_id: str, data: ReservationSlotUpdate, manager_id: str
    ) -> ReservationSlotResponse:
        await cls._verify_ownership(restaurant_id, manager_id)
        slot = await SlotRepository.find_by_id(slot_id)
        if not slot or slot["restaurant_id"] != restaurant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")

        update_data = data.model_dump(exclude_none=True)
        if "status" in update_data and hasattr(update_data["status"], "value"):
            update_data["status"] = update_data["status"].value
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        updated = await SlotRepository.update(slot_id, update_data)
        return cls._to_response(updated)

    @classmethod
    async def delete(
        cls, restaurant_id: str, slot_id: str, manager_id: str
    ) -> None:
        await cls._verify_ownership(restaurant_id, manager_id)
        slot = await SlotRepository.find_by_id(slot_id)
        if not slot or slot["restaurant_id"] != restaurant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
        await ReservationRepository.cancel_by_slot(slot_id)
        await SlotRepository.delete(slot_id)

    @staticmethod
    async def _verify_ownership(restaurant_id: str, manager_id: str) -> dict:
        restaurant = await RestaurantRepository.find_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        if restaurant["manager_id"] != manager_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")
        return restaurant

    @staticmethod
    def _to_response(doc: dict) -> ReservationSlotResponse:
        return ReservationSlotResponse(
            id=doc["_id"],
            restaurant_id=doc["restaurant_id"],
            table_id=doc["table_id"],
            start_at=doc["start_at"],
            end_at=doc["end_at"],
            status=doc["status"],
        )
