from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class SpecialOccasion(str, Enum):
    birthday = "birthday"
    anniversary = "anniversary"
    date_night = "date_night"
    engagement = "engagement"
    business_dinner = "business_dinner"
    family_celebration = "family_celebration"


class ReservationCreate(BaseModel):
    restaurant_id: str
    slot_id: str
    party_size: int = Field(..., ge=1, le=50)
    special_occasion: SpecialOccasion | None = None
    guest_note: str = Field("", max_length=500)


class ReservationUpdate(BaseModel):
    status: ReservationStatus | None = None
    slot_id: str | None = None
    party_size: int | None = Field(None, ge=1, le=50)
    special_occasion: SpecialOccasion | None = None
    guest_note: str | None = Field(None, max_length=500)


class ReservationInDB(BaseModel):
    id: str = Field(..., alias="_id")
    restaurant_id: str
    user_id: str
    slot_id: str
    party_size: int
    status: ReservationStatus
    special_occasion: SpecialOccasion | None
    guest_note: str
    created_at: datetime
    updated_at: datetime

    model_config = {"populate_by_name": True}


class ReservationResponse(BaseModel):
    id: str
    restaurant_id: str
    user_id: str
    slot_id: str
    party_size: int
    status: ReservationStatus
    special_occasion: SpecialOccasion | None
    guest_note: str
    created_at: datetime
    updated_at: datetime
    restaurant_name: str | None = None
    table_name: str | None = None
    table_type: str | None = None
    slot_start: datetime | None = None
    slot_end: datetime | None = None
    user_name: str | None = None
