from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.reservation import ReservationCreate, ReservationResponse, ReservationUpdate
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.slot_repository import SlotRepository
from app.repositories.table_repository import TableRepository
from app.repositories.user_repository import UserRepository


class ReservationService:
    @classmethod
    async def list_by_user(
        cls, user_id: str, res_status: str | None = None
    ) -> list[ReservationResponse]:
        docs = await ReservationRepository.find_by_user(user_id, status=res_status)
        return [await cls._to_response(d, enrich=True) for d in docs]

    @classmethod
    async def list_by_restaurant(
        cls,
        restaurant_id: str,
        manager_id: str,
        res_status: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[ReservationResponse]:
        restaurant = await RestaurantRepository.find_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        if restaurant["manager_id"] != manager_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")
        docs = await ReservationRepository.find_by_restaurant(restaurant_id, status=res_status)
        enriched = [await cls._to_response(d, enrich=True) for d in docs]
        if date_from or date_to:
            filtered = []
            for r in enriched:
                if r.slot_start is None:
                    continue
                if date_from and r.slot_start < date_from:
                    continue
                if date_to and r.slot_start >= date_to:
                    continue
                filtered.append(r)
            return filtered
        return enriched

    @classmethod
    async def get_by_id(cls, reservation_id: str, user_id: str, role: str) -> ReservationResponse:
        doc = await ReservationRepository.find_by_id(reservation_id)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
        if role != "admin" and doc["user_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your reservation")
        return await cls._to_response(doc, enrich=True)

    @classmethod
    async def create(cls, data: ReservationCreate, user_id: str) -> ReservationResponse:
        slot = await SlotRepository.find_by_id(data.slot_id)
        if not slot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
        if slot["status"] != "open":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slot is not open")
        if slot["restaurant_id"] != data.restaurant_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slot does not belong to this restaurant")

        table = await TableRepository.find_by_id(slot["table_id"])
        if not table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")

        if data.party_size > table["capacity"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A létszám meghaladja az asztal kapacitását ({table['capacity']} fő)",
            )

        now = datetime.now(timezone.utc)
        doc = {
            "restaurant_id": data.restaurant_id,
            "user_id": user_id,
            "slot_id": data.slot_id,
            "party_size": data.party_size,
            "status": "pending",
            "special_occasion": data.special_occasion.value if data.special_occasion else None,
            "guest_note": data.guest_note,
            "created_at": now,
            "updated_at": now,
        }
        created = await ReservationRepository.create(doc)
        await SlotRepository.update(data.slot_id, {"status": "closed"})
        return await cls._to_response(created, enrich=True)

    @classmethod
    async def update_status(
        cls,
        reservation_id: str,
        data: ReservationUpdate,
        user_id: str,
        role: str,
    ) -> ReservationResponse:
        doc = await ReservationRepository.find_by_id(reservation_id)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

        if role == "admin":
            restaurant = await RestaurantRepository.find_by_id(doc["restaurant_id"])
            if not restaurant or restaurant["manager_id"] != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant's reservation")
        elif doc["user_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your reservation")

        old_slot_id = doc["slot_id"]
        old_status = doc["status"]

        update_data = data.model_dump(exclude_none=True)
        if "status" in update_data:
            new_status = update_data["status"]
            if hasattr(new_status, "value"):
                new_status = new_status.value
                update_data["status"] = new_status
            if role == "guest" and new_status != "cancelled":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Guests can only cancel reservations",
                )
        if "slot_id" in update_data:
            if role != "admin":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can change slot")
            new_slot = await SlotRepository.find_by_id(update_data["slot_id"])
            if not new_slot:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="New slot not found")
            if new_slot["status"] != "open":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New slot is not open")
        if "special_occasion" in update_data and update_data["special_occasion"] is not None:
            if hasattr(update_data["special_occasion"], "value"):
                update_data["special_occasion"] = update_data["special_occasion"].value

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        update_data["updated_at"] = datetime.now(timezone.utc)
        updated = await ReservationRepository.update(reservation_id, update_data)

        resolved_status = update_data.get("status", old_status)
        new_slot_id = update_data.get("slot_id", old_slot_id)

        if resolved_status == "cancelled" and old_status != "cancelled":
            await SlotRepository.update(old_slot_id, {"status": "open"})
        elif "slot_id" in update_data and update_data["slot_id"] != old_slot_id:
            await SlotRepository.update(old_slot_id, {"status": "open"})
            await SlotRepository.update(new_slot_id, {"status": "closed"})

        return await cls._to_response(updated, enrich=True)

    @classmethod
    async def delete(cls, reservation_id: str, user_id: str, role: str) -> None:
        doc = await ReservationRepository.find_by_id(reservation_id)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

        if role == "admin":
            restaurant = await RestaurantRepository.find_by_id(doc["restaurant_id"])
            if not restaurant or restaurant["manager_id"] != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant's reservation")
        elif doc["user_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your reservation")

        if doc["status"] != "cancelled":
            await SlotRepository.update(doc["slot_id"], {"status": "open"})
        await ReservationRepository.delete(reservation_id)

    @staticmethod
    async def _to_response(doc: dict, enrich: bool = False) -> ReservationResponse:
        resp = ReservationResponse(
            id=doc["_id"],
            restaurant_id=doc["restaurant_id"],
            user_id=doc["user_id"],
            slot_id=doc["slot_id"],
            party_size=doc["party_size"],
            status=doc["status"],
            special_occasion=doc.get("special_occasion"),
            guest_note=doc.get("guest_note", ""),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )
        if enrich:
            restaurant = await RestaurantRepository.find_by_id(doc["restaurant_id"])
            if restaurant:
                resp.restaurant_name = restaurant["name"]
            user = await UserRepository.find_by_id(doc["user_id"])
            if user:
                resp.user_name = user.get("full_name")
            slot = await SlotRepository.find_by_id(doc["slot_id"])
            if slot:
                resp.slot_start = slot.get("start_at")
                resp.slot_end = slot.get("end_at")
                table = await TableRepository.find_by_id(slot["table_id"])
                if table:
                    resp.table_name = table["name"]
                    resp.table_type = table.get("table_type")
        return resp
