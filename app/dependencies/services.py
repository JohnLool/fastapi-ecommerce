from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.services.mongo_services.category_service import CategoryService
from app.services.mongo_services.product_service import ProductService
from app.services.role_request_service import RoleRequestService
from app.services.shop_service import ShopService
from app.services.user_service import UserService


async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_session)],
) -> UserService:
    return UserService(db)

async def get_shop_service(
        db: Annotated[AsyncSession, Depends(get_session)],
) -> ShopService:
    return ShopService(db)

async def get_role_request_service(
        db: Annotated[AsyncSession, Depends(get_session)],
) -> RoleRequestService:
    return RoleRequestService(db)

async def get_category_service() -> CategoryService:
    return CategoryService()

async def get_product_service() -> ProductService:
    return ProductService()