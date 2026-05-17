from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SlotStatus(str, Enum):
    open = "open"
    closed = "closed"


class ReservationSlotCreate(BaseModel):
    table_id: str
    start_at: datetime
    end_at: datetime
    status: SlotStatus = SlotStatus.open


class ReservationSlotUpdate(BaseModel):
    table_id: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    status: SlotStatus | None = None


class ReservationSlotInDB(BaseModel):
    id: str = Field(..., alias="_id")
    restaurant_id: str
    table_id: str
    start_at: datetime
    end_at: datetime
    status: SlotStatus

    model_config = {"populate_by_name": True}


class ReservationSlotResponse(BaseModel):
    id: str
    restaurant_id: str
    table_id: str
    start_at: datetime
    end_at: datetime
    status: SlotStatus
