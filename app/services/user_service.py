from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repo import UserRepository

from app.schemas.user import UserOut, UserCreate, UserUpdate

from app.services.base_service import BaseService
from app.utils.logger import logger
from app.utils.password_utils import verify_password, hash_password


class UserService(BaseService[UserRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserRepository(db), UserOut)

    async def create(self, user_data: UserCreate) -> Optional[UserOut]:
        data = user_data.model_dump()
        if "password" in data and data["password"]:
            data["hashed_password"] = await hash_password(user_data.password)
            del data["password"]
        return await super().create(data)

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserOut]:
        user = await self.repository.get_by_id(user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = await hash_password(update_data["password"])
            del update_data["password"]

        return await super().update(user_id, update_data)

    async def get_by_username(self, username: str) -> Optional[UserOut]:
        record = await self.repository.get_by_username(username)
        if not record:
            return None
        return UserOut.model_validate(record)

    async def get_by_username_orm(self, username: str) -> Optional[UserOut]:
        record = await self.repository.get_by_username(username)
        return record

    async def authenticate_user(self, username: str, password: str):
        user = await self.repository.get_by_username(username)
        logger.info(f"Found user: {user}")
        if not user:
            print("User not found")
            return None

        is_valid = await verify_password(password, user.hashed_password)
        logger.info(f"Password valid: {is_valid}")

        if not is_valid:
            return None

        return user

    async def set_role(self, user_id: int):
        return await self.repository.set_role(user_id, "seller")