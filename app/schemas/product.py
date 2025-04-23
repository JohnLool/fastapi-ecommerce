from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field("")
    price: float = Field(..., ge=0)
    in_stock: int = Field(0, ge=0)
    category_id: Optional[PydanticObjectId] = Field(None)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    price: Optional[float] = Field(None, ge=0)
    in_stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[PydanticObjectId] = Field(None)

class ProductOut(ProductBase):
    id: PydanticObjectId = Field(..., alias="_id")
    slug: str = Field(...)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True