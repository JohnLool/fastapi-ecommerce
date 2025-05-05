from typing import List

from fastapi import Security, Depends, HTTPException, APIRouter

from app.dependecies.auth import require_scopes
from app.dependecies.services import get_role_request_service
from app.schemas.role_request import RoleRequestOut
from app.services.role_request_service import RoleRequestService
from app.utils.exceptions import RequestNotFoundError, RequestAlreadyProcessedError


router = APIRouter(prefix="/role-requests", tags=["role_requests"])

@router.patch(
    "/{request_id}",
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

@router.get(
    "",
    response_model=List[RoleRequestOut],
    dependencies=[Security(require_scopes("read:role_requests"))],
)
async def get_all_requests(
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