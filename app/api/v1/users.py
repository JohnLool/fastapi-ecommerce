from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Security
from fastapi.security import OAuth2PasswordRequestForm

from app.core.authx_security import security
from app.dependecies.auth import get_current_user, require_scopes, get_scopes_for_role
from app.dependecies.services import get_user_service, get_role_request_service
from app.models import UserOrm
from app.schemas.role_request import RoleRequestOut, RoleRequestCreate
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.services.role_request_service import RoleRequestService
from app.services.user_service import UserService
from app.utils.exceptions import DuplicateRoleRequestError, RequestNotFoundError, RequestAlreadyProcessedError, \
    ForbiddenRoleRequestError

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
        raise HTTPException(status_code=401, detail="Invalid username or password")
    scopes = get_scopes_for_role(user.role)
    token = security.create_access_token(
        uid=user.username,
        data={"user_id": user.id, "role": user.role.value, "scopes": scopes},
    )
    return {"access_token": token, "token_type": "bearer"}

@router.post("/roles/requests", response_model=RoleRequestOut)
async def create_request(
        request: RoleRequestCreate,
        current_user: UserOrm = Depends(require_scopes("create:role_request")),
        service: RoleRequestService = Depends(get_role_request_service),
):
    try:
        return await service.create_request(request, current_user)
    except DuplicateRoleRequestError:
        raise HTTPException(status_code=400, detail="Request already exists")
    except ForbiddenRoleRequestError:
        raise HTTPException(status_code=400, detail=f"You cannot request role: {request.role}")
@router.patch(
    "/roles/requests/{request_id}",
    response_model=RoleRequestOut,
    dependencies=[Security(require_scopes("update:role"))],
)
async def process_request(
        request_id: int,
        approve: bool,
        service: RoleRequestService = Depends(get_role_request_service),
):
    try:
        return await service.process_request(request_id, approve)
    except RequestNotFoundError:
        raise HTTPException(status_code=404, detail="Request not found")
    except RequestAlreadyProcessedError:
        raise HTTPException(status_code=400, detail="Request already processed")