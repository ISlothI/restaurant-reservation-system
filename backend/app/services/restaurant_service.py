from fastapi import HTTPException, status

from app.models.restaurant import RestaurantCreate, RestaurantResponse, RestaurantUpdate
from app.repositories.restaurant_repository import RestaurantRepository


class RestaurantService:
    @classmethod
    async def list_all(cls, active_only: bool = True) -> list[RestaurantResponse]:
        filters = {"is_active": True} if active_only else {}
        docs = await RestaurantRepository.find_all(filters)
        return [cls._to_response(d) for d in docs]

    @classmethod
    async def get_by_id(cls, restaurant_id: str) -> RestaurantResponse:
        doc = await RestaurantRepository.find_by_id(restaurant_id)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        return cls._to_response(doc)

    @classmethod
    async def get_by_manager(cls, manager_id: str) -> RestaurantResponse | None:
        doc = await RestaurantRepository.find_by_manager(manager_id)
        if not doc:
            return None
        return cls._to_response(doc)

    @classmethod
    async def create(cls, data: RestaurantCreate, manager_id: str) -> RestaurantResponse:
        existing = await RestaurantRepository.find_by_manager(manager_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Admin already has a restaurant",
            )
        doc = {
            "manager_id": manager_id,
            "name": data.name,
            "description": data.description,
            "address": data.address,
            "contact": data.contact,
            "opening_hours": data.opening_hours,
            "services": [s.value for s in data.services],
            "is_active": data.is_active,
        }
        created = await RestaurantRepository.create(doc)
        return cls._to_response(created)

    @classmethod
    async def update(
        cls, restaurant_id: str, data: RestaurantUpdate, manager_id: str
    ) -> RestaurantResponse:
        restaurant = await RestaurantRepository.find_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        if restaurant["manager_id"] != manager_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")

        update_data = data.model_dump(exclude_none=True)
        if "services" in update_data:
            update_data["services"] = [s.value if hasattr(s, "value") else s for s in update_data["services"]]
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        updated = await RestaurantRepository.update(restaurant_id, update_data)
        return cls._to_response(updated)

    @classmethod
    async def delete(cls, restaurant_id: str, manager_id: str) -> None:
        restaurant = await RestaurantRepository.find_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        if restaurant["manager_id"] != manager_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your restaurant")
        await RestaurantRepository.delete(restaurant_id)

    @staticmethod
    def _to_response(doc: dict) -> RestaurantResponse:
        return RestaurantResponse(
            id=doc["_id"],
            manager_id=doc["manager_id"],
            name=doc["name"],
            description=doc.get("description", ""),
            address=doc["address"],
            contact=doc.get("contact", ""),
            opening_hours=doc.get("opening_hours", ""),
            services=doc.get("services", []),
            is_active=doc.get("is_active", True),
        )
