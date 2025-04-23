from typing import Optional

from beanie import Document, Indexed, before_event, Insert, Replace, PydanticObjectId, Link
from pydantic import Field
from datetime import datetime, timezone
from slugify import slugify
from uuid import uuid4

from app.models.category import Category


class Product(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    name: str = Field(...)
    slug: Indexed(str, unique=True) = Field(None)
    description: str = Field("")
    price: float = Field(..., ge=0)
    in_stock: int = Field(0, ge=0)

    category: Optional[Link[Category]] = Field(None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "products"

    @before_event(Insert)
    def on_insert(self):
        now = datetime.now(timezone.utc)
        self.created_at = now
        self.updated_at = now
        base = slugify(self.name)
        suf = uuid4().hex[:8]
        self.slug = f"{base}-{suf}"

    @before_event(Replace)
    def on_replace(self):
        self.updated_at = datetime.now(timezone.utc)
