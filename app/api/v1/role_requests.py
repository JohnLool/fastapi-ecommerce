from typing import List

from fastapi import Security, Depends, HTTPException, APIRouter

from app.dependencies.auth import require_scopes
from app.dependencies.services import get_role_request_service, get_user_service
from app.schemas.role_request import RoleRequestOut
from app.services.role_request_service import RoleRequestService
from app.services.user_service import UserService
from app.utils.exceptions import RequestNotFoundError, RequestAlreadyProcessedError


router = APIRouter(prefix="/role-requests", tags=["role_requests"])

@router.patch(
    "/{request_id}/reject",
    response_model=RoleRequestOut,
    dependencies=[Security(require_scopes("update:role"))],
)
async def reject_request(
        request_id: int,
        service: RoleRequestService = Depends(get_role_request_service),
):
    try:
        return await service.process_request(request_id, False)
    except RequestNotFoundError:
        raise HTTPException(status_code=404, detail="Request not found")
    except RequestAlreadyProcessedError:
        raise HTTPException(status_code=400, detail="Request already processed")

@router.patch(
    "/{request_id}/approve",
    response_model=RoleRequestOut,
    dependencies=[Security(require_scopes("update:role"))],
)
async def approve_request(
        request_id: int,
        role_req_svc: RoleRequestService = Depends(get_role_request_service),
        user_svc: UserService = Depends(get_user_service),
):
    try:
        request =  await role_req_svc.process_request(request_id, True)
        await user_svc.set_role(request.user_id)
        return request
    except RequestNotFoundError:
        raise HTTPException(status_code=404, detail="Request not found")
    except RequestAlreadyProcessedError:
        raise HTTPException(status_code=400, detail="Request already processed")

@router.get(
    "",
    response_model=List[RoleRequestOut],
    dependencies=[Security(require_scopes("read:role_requests"))],
)
async def list_requests(
        service: RoleRequestService = Depends(get_role_request_service),
):
    return await service.get_all()

@router.get(
    "/{request_id}",
    response_model=RoleRequestOut,
    dependencies=[Security(require_scopes("read:role_requests"))],
)
async def get_request_by_id(
        request_id: int,
        service: RoleRequestService = Depends(get_role_request_service),
):
    return await service.get_by_id(request_id)