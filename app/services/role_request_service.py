from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RoleRequestOrm
from app.models.role_request import RequestStatus
from app.repositories.role_request_repo import RoleRequestRepository
from app.repositories.user_repo import UserRepository
from app.schemas.role_request import RoleRequestOut, RoleRequestCreate
from app.services.base_service import BaseService
from app.utils.exceptions import RequestNotFoundError, RequestAlreadyProcessedError, DuplicateRoleRequestError


class RoleRequestService(BaseService[RoleRequestRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(RoleRequestRepository(db), RoleRequestOut)
        self.user_repo = UserRepository(db)

    async def process_request(self, request_id: int, approve: bool) -> RoleRequestOut:
        req = await self.repository.get_by_id(request_id)
        if not req:
            raise RequestNotFoundError()
        if req.status != RequestStatus.pending:
            raise RequestAlreadyProcessedError()

        if approve:
            await self.repository.set_status(request_id, RequestStatus.approved)
            await self.user_repo.set_role(req.user_id, req.desired_role)
        else:
            await self.repository.set_status(request_id, RequestStatus.rejected)

        return await super().get_by_id(request_id)

    async def create_request(self, data: RoleRequestCreate, user_id: int) -> RoleRequestOut:
        existing = await self.repository.get_one_by_filters([
            RoleRequestOrm.user_id == user_id,
            RoleRequestOrm.desired_role == data.role,
            RoleRequestOrm.status == RequestStatus.pending
        ])
        if existing:
            raise DuplicateRoleRequestError()

        request_dict = data.model_dump()
        request_dict['user_id'] = user_id

        return await super().create(request_dict)