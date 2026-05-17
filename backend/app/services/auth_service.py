from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import HTTPException, status
from jose import jwt

from app.config import settings
from app.models.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository


class AuthService:
    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def _verify_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    @staticmethod
    def _create_token(user_id: str, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_expiration_minutes
        )
        payload = {"sub": user_id, "role": role, "exp": expire}
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    @classmethod
    async def register(cls, data: UserCreate) -> UserResponse:
        existing = await UserRepository.find_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user_doc = {
            "email": data.email,
            "password_hash": cls._hash_password(data.password),
            "full_name": data.full_name,
            "phone": data.phone,
            "role": data.role.value,
        }
        created = await UserRepository.create(user_doc)
        return UserResponse(
            id=created["_id"],
            email=created["email"],
            full_name=created["full_name"],
            phone=created["phone"],
            role=created["role"],
        )

    @classmethod
    async def login(cls, email: str, password: str) -> dict:
        user = await UserRepository.find_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not cls._verify_password(password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        user_id = str(user["_id"])
        token = cls._create_token(user_id, user["role"])
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user_id,
                email=user["email"],
                full_name=user["full_name"],
                phone=user["phone"],
                role=user["role"],
            ).model_dump(),
        }
