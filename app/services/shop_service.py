from typing import Optional
from uuid import uuid4

from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ShopOrm
from app.repositories.shop_repo import ShopRepository
from app.schemas.shop import ShopOut, ShopCreate, ShopUpdate

from app.services.base_service import BaseService


class ShopService(BaseService[ShopRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(ShopRepository(db), ShopOut)

    async def get_by_slug(self, slug: str) -> ShopOut:
        record = await self.repository.get_by_slug(slug)
        if not record:
            return None
        return ShopOut.model_validate(record)

    async def create_with_owner(self, shop_data: ShopCreate, owner_id: int) -> Optional[ShopOut]:
        shop_dict = shop_data.model_dump()
        shop_dict['owner_id'] = owner_id

        if "name" in shop_dict:
            base = slugify(shop_dict["name"])
            suf = uuid4().hex[:8]
            shop_dict["slug"] = f"{base}-{suf}"

        return await super().create(shop_dict)

    async def update(self, shop_id: int, shop_data: ShopUpdate) -> ShopOut:
        shop_dict = shop_data.model_dump(exclude_unset=True)

        existing_shop: ShopOrm = await self.repository.get_by_id(shop_id)
        if not existing_shop:
            return None

        if "name" in shop_dict and shop_dict["name"] != existing_shop.name:
            base = slugify(shop_dict["name"])
            suf = uuid4().hex[:8]
            shop_dict["slug"] = f"{base}-{suf}"

        return await super().update(shop_id, shop_dict)