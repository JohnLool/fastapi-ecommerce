from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from app.models.order import OrderStatus


class OrderItemOut(BaseModel):
    id: int
    product_slug: str
    quantity: int
    title_snapshot: str
    price_snapshot: Decimal
    image_snapshot: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    shipping_address: str
    payment_method: Optional[str] = None

class OrderOut(BaseModel):
    id: int
    user_id: int
    status: OrderStatus

    subtotal: Decimal
    discount_total: Decimal
    delivery_fee: Decimal
    grand_total: Decimal

    payment_method: Optional[str] = None
    payment_status: Optional[str] = None

    paid_at: Optional[datetime] = None
    shipping_address: str
    tracking_number: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    items: List[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)