from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Security

from app.dependecies.auth import require_scopes
from app.dependecies.services import get_product_service
from app.dependecies.validate_ownership import validate_shop_ownership, validate_product_ownership
from app.schemas.shop import ShopOut
from app.services.mongo_services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut

router = APIRouter(prefix="/product", tags=["products"])

@router.get("", response_model=List[ProductOut])
async def list_products(
    service: ProductService = Depends(get_product_service)
):
    return await service.get_all()

@router.get("/{product_slug}", response_model=ProductOut)
async def get_product_by_slug(
    product_slug: str,
    service: ProductService = Depends(get_product_service)
):
    product = await service.get_by_slug(product_slug)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post(
    "",
    response_model=ProductOut,
    dependencies=[Security(require_scopes("create:product"))],
)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
    shop: ShopOut = Depends(validate_shop_ownership),
):
    product = await service.create_with_shop(data, shop.id)
    if not product:
        raise HTTPException(status_code=400, detail="Product creation failed")
    return product

@router.put(
    "/{product_slug}",
    response_model=ProductOut,
    dependencies=[Security(require_scopes("update:product"))],
)
async def update_product_by_slug(
    update_data: ProductUpdate,
    product: ProductOut = Depends(validate_product_ownership),
    service: ProductService = Depends(get_product_service)
):
    updated = await service.update(product.id, update_data)
    if not updated:
        raise HTTPException(status_code=400, detail="Update failed")
    return updated

@router.delete(
    "/{product_slug}",
    response_model=ProductOut,
    dependencies=[Security(require_scopes("delete:product"))],
)
async def delete_product_by_slug(
    product: ProductOut = Depends(validate_product_ownership),
    service: ProductService = Depends(get_product_service)
):
    deleted = await service.delete(product.id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Deletion failed")
    return deleted