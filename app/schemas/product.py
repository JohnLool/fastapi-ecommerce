from typing import Any, Dict, Optional, Union
from decimal import Decimal
from datetime import datetime

from beanie import PydanticObjectId
from bson import Decimal128
from pydantic import BaseModel, Field, ConfigDict, model_validator


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field("", max_length=1000)
    price: Decimal = Field(..., ge=0)
    in_stock: int = Field(0, ge=0)
    category: Optional[str] = Field(..., max_length=255)

    attributes: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, ge=0)
    in_stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(..., max_length=255)
    attributes: Optional[Dict[str, Any]] = None

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

    @model_validator(mode="before")
    @classmethod
    def convert_bson_decimal128_to_decimal(cls, data: dict[str, Any]) -> Any:
        for field in data:
            if isinstance(data[field], Decimal128):
                data[field] = data[field].to_decimal()
        return data