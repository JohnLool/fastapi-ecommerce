from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict



class ProductBase(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field("")
    price: float = Field(..., ge=0)
    in_stock: int = Field(0, ge=0)
    category: Optional[str] = Field(...)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    price: Optional[float] = Field(None, ge=0)
    in_stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(...)

class ProductOut(ProductBase):
    id: PydanticObjectId = Field(..., alias="_id")
    seller_id: int
    slug: str = Field(...)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        validate_by_name=True,
        from_attributes=True
    )