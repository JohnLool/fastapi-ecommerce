from datetime import datetime
from decimal import Decimal
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field("", max_length=1000)
    price: Decimal = Field(..., ge=0)
    in_stock: int = Field(0, ge=0)
    category: Optional[str] = Field(..., max_length=255)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, ge=0)
    in_stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(..., max_length=255)

class ProductOut(ProductBase):
    id: PydanticObjectId = Field(..., alias="_id")
    shop_id: int = Field(...)
    slug: str = Field(...)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    image_url: Optional[str] = None

    model_config = ConfigDict(
        validate_by_name=True,
        from_attributes=True
    )