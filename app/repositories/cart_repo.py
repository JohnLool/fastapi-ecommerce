from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cart import CartOrm
from app.repositories.base_repo import BaseRepository


class CartRepository(BaseRepository[CartOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(CartOrm, session)

    async def get_by_user_id(self, user_id: int) -> Optional[CartOrm]:
        return await self.get_one_by_filters(self.model.user_id == user_id)

    async def get_or_create_by_user(self, user_id: int) -> CartOrm:
        cart = await self.get_by_user_id(user_id)
        if cart:
            return cart
        return await self.create({"user_id": user_id})
