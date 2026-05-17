from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    admin = "admin"
    guest = "guest"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field("", max_length=20)
    role: UserRole = UserRole.guest


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInDB(BaseModel):
    id: str = Field(..., alias="_id")
    email: str
    password_hash: str
    full_name: str
    phone: str
    role: UserRole

    model_config = {"populate_by_name": True}


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    phone: str
    role: UserRole
