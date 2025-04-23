from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(...)

class CategoryCreate(CategoryBase):
    description: Optional[str] = Field(None)

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)

class CategoryOut(CategoryBase):
    id: PydanticObjectId = Field(..., alias="_id")
    slug: str = Field(...)
    description: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True