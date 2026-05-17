from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.middleware.auth import get_current_user, require_role
from app.models.reservation import ReservationCreate, ReservationResponse, ReservationUpdate
from app.services.reservation_service import ReservationService

router = APIRouter()


@router.get("/my", response_model=list[ReservationResponse])
async def list_my_reservations(
    status: str | None = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return await ReservationService.list_by_user(current_user["_id"], res_status=status)


@router.get(
    "/restaurant/{restaurant_id}", response_model=list[ReservationResponse]
)
async def list_restaurant_reservations(
    restaurant_id: str,
    status: str | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    admin: dict = Depends(require_role("admin")),
):
    return await ReservationService.list_by_restaurant(
        restaurant_id, admin["_id"], res_status=status,
        date_from=date_from, date_to=date_to,
    )


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(
    reservation_id: str,
    current_user: dict = Depends(get_current_user),
):
    return await ReservationService.get_by_id(
        reservation_id, current_user["_id"], current_user["role"]
    )


@router.post("", response_model=ReservationResponse, status_code=201)
async def create_reservation(
    data: ReservationCreate,
    current_user: dict = Depends(get_current_user),
):
    return await ReservationService.create(data, current_user["_id"])


@router.patch("/{reservation_id}", response_model=ReservationResponse)
async def update_reservation(
    reservation_id: str,
    data: ReservationUpdate,
    current_user: dict = Depends(get_current_user),
):
    return await ReservationService.update_status(
        reservation_id, data, current_user["_id"], current_user["role"]
    )


@router.delete("/{reservation_id}", status_code=204)
async def delete_reservation(
    reservation_id: str,
    current_user: dict = Depends(get_current_user),
):
    await ReservationService.delete(
        reservation_id, current_user["_id"], current_user["role"]
    )
