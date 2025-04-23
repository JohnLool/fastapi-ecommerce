from beanie import Document, Indexed, before_event, Insert
from pydantic import Field
from datetime import datetime, timezone
from slugify import slugify
from uuid import uuid4

class Product(Document):
    name: str = Field(...)
    slug: Indexed(str, unique=True) = Field(None)
    description: str = Field("")
    price: float = Field(..., ge=0)
    in_stock: int = Field(0, ge=0)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "products"

    @before_event(Insert)
    def set_slug_and_date(self):
        self.created_at = datetime.now(timezone.utc)
        base = slugify(self.name)
        suffix = uuid4().hex[:8]
        self.slug = f"{base}-{suffix}"
