from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.authx_security import security
from app.dependecies.auth import get_current_user, require_scopes, get_scopes_for_role
from app.dependecies.services import get_user_service
from app.models import UserOrm
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["user"])

@router.post("", response_model=UserOut, status_code=201)
async def create_user(
        user: UserCreate,
        user_service: UserService = Depends(get_user_service),
):
    return await user_service.create(user)

@router.get("/profile", response_model=UserOut)
async def get_user_profile(
        user_service: UserService = Depends(get_user_service),
        current_user: UserOrm = Depends(require_scopes("read:profile"))
):
    return await user_service.get_by_id(current_user.id)
@router.patch("", response_model=UserOut)
async def update_user(
        user_data: UserUpdate,
        user_service: UserService = Depends(get_user_service),
        current_user: UserOrm = Depends(get_current_user),
):
    return await user_service.update(current_user.id, user_data)

@router.delete("", status_code=204)
async def delete_user(
        current_user: UserOrm = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.delete(current_user.id)

@router.post("/login", tags=["auth"])
async def login_for_user_tokens(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    scopes = get_scopes_for_role(user.role)
    token = security.create_access_token(
        uid=user.username,
        data={"user_id": user.id, "role": user.role.value, "scopes": scopes},
    )
    return {"access_token": token, "token_type": "bearer"}
