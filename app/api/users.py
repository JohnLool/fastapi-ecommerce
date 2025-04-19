from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.authx_security import security
from app.dependecies.services import get_user_service
from app.schemas.user import UserOut, UserCreate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserOut)
async def create_user(
        user: UserCreate,
        user_service: UserService = Depends(get_user_service),
):
    return await user_service.create(user)

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

    token = security.create_access_token(uid=user.username)
    return {"access_token": token}
