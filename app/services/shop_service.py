from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.shop_repo import ShopRepository
from app.schemas.user import UserOut

from app.services.base_service import BaseService


class ShopService(BaseService[ShopRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(ShopRepository(db), UserOut)
