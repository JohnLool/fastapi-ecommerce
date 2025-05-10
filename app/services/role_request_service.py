from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RoleRequestOrm
from app.models.role_request import RequestStatus
from app.models.user import Role, UserOrm
from app.repositories.role_request_repo import RoleRequestRepository

from app.schemas.role_request import RoleRequestOut, RoleRequestCreate
from app.services.base_service import BaseService
from app.utils.exceptions import RequestNotFoundError, RequestAlreadyProcessedError, DuplicateRoleRequestError, \
    ForbiddenRoleRequestError


class RoleRequestService(BaseService[RoleRequestRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(RoleRequestRepository(db), RoleRequestOut)

    async def process_request(self, request_id: int, approve: bool) -> RoleRequestOut:
        req = await self.repository.get_by_id(request_id)
        if not req:
            raise RequestNotFoundError()
        if req.status != RequestStatus.pending:
            raise RequestAlreadyProcessedError()

        if approve:
            await self.repository.set_status(request_id, RequestStatus.approved)
        else:
            await self.repository.set_status(request_id, RequestStatus.rejected)

        return await super().get_by_id(request_id)

    async def create_request(self, request: RoleRequestCreate, user: UserOrm) -> RoleRequestOut:
        if request.desired_role != Role.seller or user.role != Role.customer:
            raise ForbiddenRoleRequestError()

        filters = [
            RoleRequestOrm.user_id == user.id,
            RoleRequestOrm.desired_role == request.desired_role,
            RoleRequestOrm.status == RequestStatus.pending,
        ]
        existing = await self.repository.get_one_by_filters(*filters)

        if existing:
            raise DuplicateRoleRequestError()

        request_dict = request.model_dump()
        request_dict['user_id'] = user.id

        return await super().create(request_dict)