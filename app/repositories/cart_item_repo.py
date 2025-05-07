from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cart_item import CartItemOrm
from app.repositories.base_repo import BaseRepository


class CartItemRepository(BaseRepository[CartItemOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(CartItemOrm, session)

    async def get_for_cart_and_product(self, cart_id: int, product_id: str) -> Optional[CartItemOrm]:
        return await self.get_one_by_filters(
            self.model.cart_id == cart_id,
            self.model.product_id == product_id
        )
