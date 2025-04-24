from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependecies.services import get_category_service
from app.services.mongo_services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut

router = APIRouter(prefix="/category", tags=["categories"])

@router.get("", response_model=List[CategoryOut])
async def list_categories(
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_all()

@router.get("/{slug}", response_model=CategoryOut)
async def get_category_by_slug(
    slug: str,
    service: CategoryService = Depends(get_category_service)
):
    category = await service.get_by_slug(slug)
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

@router.put("/{slug}", response_model=CategoryOut)
async def update_category_by_slug(
    slug: str,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service)
):
    existing = await service.get_by_slug(slug)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    updated = await service.update(existing.id, data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update failed")
    return updated

@router.delete("/{slug}", response_model=CategoryOut)
async def delete_category_by_slug(
    slug: str,
    service: CategoryService = Depends(get_category_service)
):
    existing = await service.get_by_slug(slug)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    deleted = await service.delete(existing.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Deletion failed")
    return deleted