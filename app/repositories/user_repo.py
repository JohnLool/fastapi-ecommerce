from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.repositories.base_repo import BaseRepository
from app.models.user import UserOrm
from app.utils.logger import logger


class UserRepository(BaseRepository[UserOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserOrm, session)

    async def get_by_email(self, email: str, *filters, options=None) -> Optional[UserOrm]:
        return await super().get_by_field('email', email, *filters, options=options)

    async def get_by_username(self, username: str, *filters, options=None) -> Optional[UserOrm]:
        return await super().get_by_field('username', username, *filters, options=options)

    async def set_role(self, user_id: int, new_role: str) -> UserOrm:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        try:
            user.role = new_role
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            logger.error(f"Failed to set role on User id {user_id}: {e}")
            await self.session.rollback()
            raise