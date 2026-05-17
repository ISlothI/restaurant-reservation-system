from fastapi import APIRouter, Depends, Query

from app.middleware.auth import require_role
from app.models.reservation_slot import (
    ReservationSlotCreate,
    ReservationSlotResponse,
    ReservationSlotUpdate,
)
from app.services.slot_service import SlotService

router = APIRouter()


@router.get(
    "/{restaurant_id}/slots", response_model=list[ReservationSlotResponse]
)
async def list_slots(
    restaurant_id: str, status: str | None = Query(None)
):
    return await SlotService.list_by_restaurant(restaurant_id, slot_status=status)


@router.get(
    "/{restaurant_id}/slots/{slot_id}", response_model=ReservationSlotResponse
)
async def get_slot(restaurant_id: str, slot_id: str):
    return await SlotService.get_by_id(slot_id)


@router.post(
    "/{restaurant_id}/slots",
    response_model=ReservationSlotResponse,
    status_code=201,
)
async def create_slot(
    restaurant_id: str,
    data: ReservationSlotCreate,
    admin: dict = Depends(require_role("admin")),
):
    return await SlotService.create(restaurant_id, data, admin["_id"])


@router.put(
    "/{restaurant_id}/slots/{slot_id}",
    response_model=ReservationSlotResponse,
)
async def update_slot(
    restaurant_id: str,
    slot_id: str,
    data: ReservationSlotUpdate,
    admin: dict = Depends(require_role("admin")),
):
    return await SlotService.update(restaurant_id, slot_id, data, admin["_id"])


@router.delete("/{restaurant_id}/slots/{slot_id}", status_code=204)
async def delete_slot(
    restaurant_id: str,
    slot_id: str,
    admin: dict = Depends(require_role("admin")),
):
    await SlotService.delete(restaurant_id, slot_id, admin["_id"])
