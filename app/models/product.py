from typing import Optional

from beanie import Document, Indexed, before_event, Insert, Replace, PydanticObjectId, Link

from pydantic import Field, condecimal
from datetime import datetime, timezone

from app.models.category import Category


class Product(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    shop_id: int = Field(...)
    name: str = Field(..., min_length=1)
    slug: Indexed(str, unique=True) = Field(..., min_length=1)
    description: str = Field(default="")
    price: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(...)
    in_stock: int = Field(0, ge=0)
    image_url: Optional[str] = Field(default=None, max_length=1024)

    category: Optional[Link[Category]] = Field(None)
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)

    class Settings:
        name = "products"

    @before_event(Insert)
    def on_insert(self):
        now = datetime.now(timezone.utc)
        self.created_at = now
        self.updated_at = now

    @before_event(Replace)
    def on_replace(self):
        self.updated_at = datetime.now(timezone.utc)
