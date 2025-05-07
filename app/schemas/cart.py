from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class AddCartItemIn(BaseModel):
    product_slug: str
    quantity: int = Field(..., gt=0, le=100)

class CartItemOut(BaseModel):
    id: int
    product_slug: str
    quantity: int
    title_snapshot: str
    image_snapshot: Optional[str]
    price_snapshot: float

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