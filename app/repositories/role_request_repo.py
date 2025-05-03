from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repo import BaseRepository
from app.models.role_request import RoleRequestOrm

from app.utils.logger import logger


class RoleRequestRepository(BaseRepository[RoleRequestOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(RoleRequestOrm, session)

    async def set_status(self, request_id: int, status_value: str) -> RoleRequestOrm:
        try:
            request = await self.get_by_id(request_id)
            if not request:
                return None
            request.status = status_value
            await self.session.commit()
            await self.session.refresh(request)
            return request
        except SQLAlchemyError as e:
            logger.error(f"Error set status {self.model.__name__}: {e}")
            await self.session.rollback()
            raise