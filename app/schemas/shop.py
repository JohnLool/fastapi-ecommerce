from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ShopBase(BaseModel):
    name: str = Field(..., max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

class ShopCreate(ShopBase):
    pass

class ShopUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    deleted: Optional[bool] = None

class ShopOut(ShopBase):
    id: int = Field(...)
    seller_id: int = Field(...)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )
