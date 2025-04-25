from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependecies.auth import require_role
from app.dependecies.services import get_product_service
from app.models.user import Role, UserOrm
from app.services.mongo_services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut

router = APIRouter(prefix="/product", tags=["products"])

@router.get("", response_model=List[ProductOut])
async def list_products(
    service: ProductService = Depends(get_product_service)
):
    return await service.get_all()

@router.get("/{slug}", response_model=ProductOut)
async def get_product_by_slug(
    slug: str,
    service: ProductService = Depends(get_product_service)
):
    product = await service.get_by_slug(slug)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED,)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
    current_user: UserOrm = Depends(require_role(Role.seller, Role.admin, Role.owner))
):
    product = await service.create_with_seller(data, current_user.id)
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product creation failed")
    return product

@router.put("/{slug}", response_model=ProductOut)
async def update_product_by_slug(
    slug: str,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):
    existing = await service.get_by_slug(slug)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    updated = await service.update(existing.id, data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update failed")
    return updated

@router.delete("/{slug}", response_model=ProductOut)
async def delete_product_by_slug(
    slug: str,
    service: ProductService = Depends(get_product_service)
):
    existing = await service.get_by_slug(slug)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    deleted = await service.delete(existing.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Deletion failed")
    return deleted