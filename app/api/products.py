from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from app.dependecies.services import get_product_service
from app.services.mongo_services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut


router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[ProductOut])
async def list_products(
    service: ProductService = Depends(get_product_service)
):
    return await service.get_all()

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: PydanticObjectId,
    service: ProductService = Depends(get_product_service)
):
    product = await service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    product = await service.create(data)
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product creation failed")
    return product

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: PydanticObjectId,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):
    product = await service.update(product_id, data)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=ProductOut)
async def delete_product(
    product_id: PydanticObjectId,
    service: ProductService = Depends(get_product_service)
):
    product = await service.delete(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
