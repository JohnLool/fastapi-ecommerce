from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from app.dependecies.services import get_category_service
from app.services.mongo_services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut


router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=List[CategoryOut])
async def list_categories(
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_all()

@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(
    category_id: PydanticObjectId,
    service: CategoryService = Depends(get_category_service)
):
    category = await service.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
):
    category = await service.create(data)
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category creation failed")
    return category

@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: PydanticObjectId,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service)
):
    category = await service.update(category_id, data)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.delete("/{category_id}", response_model=CategoryOut)
async def delete_category(
    category_id: PydanticObjectId,
    service: CategoryService = Depends(get_category_service)
):
    category = await service.delete(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category