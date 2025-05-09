from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.cart_item_repo import CartItemRepository
from app.repositories.cart_repo import CartRepository
from app.repositories.mongo_repos.product_repo import ProductRepository
from app.repositories.shop_repo import ShopRepository

AsyncDB = Annotated[AsyncSession, Depends(get_session)]


async def get_cart_repo(db: AsyncDB) -> CartRepository:
    return CartRepository(db)

async def get_cart_item_repo(db: AsyncDB) -> CartItemRepository:
    return CartItemRepository(db)

async def get_shop_repo(db: AsyncDB) -> ShopRepository:
    return ShopRepository(db)

async def get_product_repo() -> ProductRepository:
    return ProductRepository()