from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255)

class CategoryCreate(CategoryBase):
    description: Optional[str] = Field(None, max_length=255)

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)

class CategoryOut(CategoryBase):
    id: PydanticObjectId = Field(..., alias="_id")
    slug: str = Field(...)
    description: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        validate_by_name=True,
        from_attributes=True
    )