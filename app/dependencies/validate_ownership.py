from fastapi import Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_shop_service, get_product_service
from app.models import UserOrm
from app.schemas.product import ProductOut
from app.schemas.shop import ShopOut
from app.services.mongo_services.product_service import ProductService
from app.services.shop_service import ShopService


async def validate_shop_ownership(
    shop_slug: str,
    current_user: UserOrm = Depends(get_current_user),
    shop_service: ShopService = Depends(get_shop_service),
) -> ShopOut:
    shop = await shop_service.get_by_slug(shop_slug)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    if shop.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return shop

async def validate_product_ownership(
    product_slug: str,
    current_user: UserOrm = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service),
    shop_service: ShopService = Depends(get_shop_service),
) -> ProductOut:
    product = await product_service.get_by_slug(product_slug)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    shop = await shop_service.get_by_id(product.shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Product's shop not found")

    if shop.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return product
