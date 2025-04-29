from fastapi import Depends, HTTPException

from app.dependecies.auth import get_current_user
from app.dependecies.services import get_shop_service
from app.models import UserOrm
from app.schemas.shop import ShopOut
from app.services.shop_service import ShopService


async def validate_shop_ownership(
    slug: str,
    current_user: UserOrm = Depends(get_current_user),
    shop_service: ShopService = Depends(get_shop_service),
) -> ShopOut:
    shop = await shop_service.get_by_slug(slug)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    if shop.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return shop
