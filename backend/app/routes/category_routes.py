from fastapi import APIRouter

from app.models.restaurant import RestaurantService as RestaurantServiceEnum

router = APIRouter()


@router.get("", response_model=list[dict])
async def list_categories():
    return [
        {"value": s.value, "label": s.value.replace("_", " ").title()}
        for s in RestaurantServiceEnum
    ]
