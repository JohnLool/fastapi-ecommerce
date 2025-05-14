from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class AddCartItemIn(BaseModel):
    product_slug: str
    quantity: int = Field(..., gt=0, le=100)

class UpdateCartItem(BaseModel):
    quantity: int = Field(..., gt=0, le=100)

class CartItemOut(BaseModel):
    id: int
    product_slug: str
    quantity: int
    title_snapshot: str
    image_snapshot: Optional[str] = None
    price_snapshot: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )

class CartOut(BaseModel):
    id: int
    user_id: int
    items: List[CartItemOut]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )