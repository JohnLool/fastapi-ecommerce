from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.authx_security import security
from app.dependecies.auth import get_current_user
from app.dependecies.services import get_user_service
from app.models import UserOrm
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserOut)
async def create_user(
        user: UserCreate,
        user_service: UserService = Depends(get_user_service),
):
    return await user_service.create(user)

@router.put("", response_model=UserOut)
async def update_user(
        user_data: UserUpdate,
        user_service: UserService = Depends(get_user_service),
        current_user: UserOrm = Depends(get_current_user),
):
    return await user_service.update(current_user.id, user_data)

@router.delete("", response_model=UserOut)
async def delete_user(
        current_user: UserOrm = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.delete(current_user.id)

@router.post("/login")
async def login_for_user_tokens(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = security.create_access_token(
        uid=user.username,
        data={"user_id": user.id, "role": user.role.value}
    )
    return {"access_token": token, "token_type": "bearer"}
