from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user, require_role
from app.models.restaurant import RestaurantCreate, RestaurantResponse, RestaurantUpdate
from app.services.restaurant_service import RestaurantService

router = APIRouter()


@router.get("", response_model=list[RestaurantResponse])
async def list_restaurants():
    return await RestaurantService.list_all()


@router.get("/my/restaurant", response_model=RestaurantResponse | None)
async def get_my_restaurant(admin: dict = Depends(require_role("admin"))):
    return await RestaurantService.get_by_manager(admin["_id"])


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(restaurant_id: str):
    return await RestaurantService.get_by_id(restaurant_id)


@router.post("", response_model=RestaurantResponse, status_code=201)
async def create_restaurant(
    data: RestaurantCreate,
    admin: dict = Depends(require_role("admin")),
):
    return await RestaurantService.create(data, admin["_id"])


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: str,
    data: RestaurantUpdate,
    admin: dict = Depends(require_role("admin")),
):
    return await RestaurantService.update(restaurant_id, data, admin["_id"])


@router.delete("/{restaurant_id}", status_code=204)
async def delete_restaurant(
    restaurant_id: str,
    admin: dict = Depends(require_role("admin")),
):
    await RestaurantService.delete(restaurant_id, admin["_id"])
