from fastapi import APIRouter, Depends, HTTPException, status

from app.middleware.auth import get_current_user
from app.models.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate):
    return await AuthService.register(data)


@router.post("/login")
async def login(data: UserLogin):
    return await AuthService.login(data.email, data.password)


@router.get("/me", response_model=UserResponse)
async def me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=current_user["_id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        phone=current_user.get("phone", ""),
        role=current_user["role"],
    )


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    data: UserUpdate,
    current_user: dict = Depends(get_current_user),
):
    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    if "email" in update_data and update_data["email"] != current_user["email"]:
        existing = await UserRepository.find_by_email(update_data["email"])
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ez az e-mail cím már foglalt")
    updated = await UserRepository.update(current_user["_id"], update_data)
    return UserResponse(
        id=updated["_id"],
        email=updated["email"],
        full_name=updated["full_name"],
        phone=updated.get("phone", ""),
        role=updated["role"],
    )
