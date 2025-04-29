from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repo import BaseRepository
from app.models.shop import ShopOrm


class ShopRepository(BaseRepository[ShopOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(ShopOrm, session)

    async def get_by_slug(self, slug: str, *filters, options=None) -> ShopOrm:
        return await super().get_by_field('slug', slug, *filters, options=options)