from enum import Enum

from pydantic import BaseModel, Field


class RestaurantService(str, Enum):
    outdoor_seating = "outdoor_seating"
    vegan_options = "vegan_options"
    gluten_free_options = "gluten_free_options"
    wheelchair_accessible = "wheelchair_accessible"
    pet_friendly = "pet_friendly"


class RestaurantCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=2000)
    address: str = Field(..., min_length=1, max_length=300)
    contact: str = Field("", max_length=100)
    opening_hours: str = Field("", max_length=200)
    services: list[RestaurantService] = Field(default_factory=list)
    is_active: bool = True


class RestaurantUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)
    address: str | None = Field(None, min_length=1, max_length=300)
    contact: str | None = Field(None, max_length=100)
    opening_hours: str | None = Field(None, max_length=200)
    services: list[RestaurantService] | None = None
    is_active: bool | None = None


class RestaurantInDB(BaseModel):
    id: str = Field(..., alias="_id")
    manager_id: str
    name: str
    description: str
    address: str
    contact: str
    opening_hours: str
    services: list[RestaurantService]
    is_active: bool

    model_config = {"populate_by_name": True}


class RestaurantResponse(BaseModel):
    id: str
    manager_id: str
    name: str
    description: str
    address: str
    contact: str
    opening_hours: str
    services: list[RestaurantService]
    is_active: bool
