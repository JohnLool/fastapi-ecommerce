from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.attribute import AttributeDefinitionIn, AttributeDefinitionOut


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=255)

class CategoryCreate(CategoryBase):
    attributes: List[AttributeDefinitionIn] = Field(default_factory=list)

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    attributes: Optional[List[AttributeDefinitionIn]] = None

class CategoryOut(CategoryBase):
    id: PydanticObjectId = Field(..., alias="_id")
    slug: str = Field(...)
    attributes: List[AttributeDefinitionOut]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        validate_by_name=True,
        from_attributes=True
    )