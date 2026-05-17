from enum import Enum

from pydantic import BaseModel, Field


class TableType(str, Enum):
    indoor = "indoor"
    outdoor = "outdoor"
    window = "window"


class TableCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    capacity: int = Field(..., ge=1, le=50)
    table_type: TableType = TableType.indoor
    is_active: bool = True


class TableUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    capacity: int | None = Field(None, ge=1, le=50)
    table_type: TableType | None = None
    is_active: bool | None = None


class TableInDB(BaseModel):
    id: str = Field(..., alias="_id")
    restaurant_id: str
    name: str
    capacity: int
    table_type: TableType
    is_active: bool

    model_config = {"populate_by_name": True}


class TableResponse(BaseModel):
    id: str
    restaurant_id: str
    name: str
    capacity: int
    table_type: TableType
    is_active: bool
