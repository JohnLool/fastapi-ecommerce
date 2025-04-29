from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repo import BaseRepository
from app.models.shop import ShopOrm


class ShopRepository(BaseRepository[ShopOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(ShopOrm, session)