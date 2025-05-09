from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security

from app.dependencies.auth import require_scopes
from app.dependencies.services import get_shop_service
from app.dependencies.validate_ownership import validate_shop_ownership
from app.models import UserOrm
from app.schemas.shop import ShopOut, ShopCreate, ShopUpdate
from app.services.shop_service import ShopService


router = APIRouter(prefix="/shops", tags=["shop"])


@router.get("", response_model=List[ShopOut])
async def get_shops(
        shop_service: ShopService = Depends(get_shop_service),
):
    return await shop_service.get_all()

@router.post("", response_model=ShopOut, status_code=201)
async def create_shop(
        shop_data: ShopCreate,
        shop_service: ShopService = Depends(get_shop_service),
        current_user: UserOrm = Depends(require_scopes("create:shop")),
):
    shop = await shop_service.create_with_owner(shop_data, current_user.id)
    if not shop:
        raise HTTPException(status_code=400, detail="Shop creation failed")
    return shop

@router.get("/{shop_slug}", response_model=ShopOut)
async def get_shop_by_slug(
        slug: str,
        shop_service: ShopService = Depends(get_shop_service),
):
    return await shop_service.get_by_slug(slug)

@router.patch(
    "/{shop_slug}",
    response_model=ShopOut,
    dependencies=[Security(require_scopes("update:shop"))],
)
async def update_shop_by_slug(
    shop_data: ShopUpdate,
    shop: ShopOut = Depends(validate_shop_ownership),
    shop_service: ShopService = Depends(get_shop_service),
):
    updated = await shop_service.update(shop.id, shop_data)
    if not updated:
        raise HTTPException(status_code=400, detail="Update failed")
    return updated


@router.delete(
    "/{shop_slug}",
    status_code=204,
    dependencies=[Security(require_scopes("delete:shop"))],
)
async def delete_shop(
        shop: ShopOut = Depends(validate_shop_ownership),
        shop_service: ShopService = Depends(get_shop_service)
):
    shop = await shop_service.delete(shop.id)
    if not shop:
        raise HTTPException(status_code=400, detail="Delete failed")
    return shop