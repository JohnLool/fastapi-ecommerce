from beanie import Document, Indexed, before_event, Insert, PydanticObjectId, Replace, Delete
from pydantic import Field
from datetime import datetime, timezone
from slugify import slugify
from typing import Optional, List

from app.schemas.attribute import AttributeDefinitionOut


class Category(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    name: Indexed(str, unique=True) = Field(...)
    slug: Indexed(str, unique=True) = Field(None)
    description: str = Field("")
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)
    attributes: List[AttributeDefinitionOut] = Field(default_factory=list)

    class Settings:
        name = "categories"

    @before_event(Insert)
    def on_insert(self):
        now = datetime.now(timezone.utc)
        self.created_at = now
        self.updated_at = now
        self.slug = slugify(self.name)
        self._generate_attribute_slugs()

    @before_event(Replace)
    def on_replace(self):
        self.updated_at = datetime.now(timezone.utc)
        self.slug = slugify(self.name)
        self._generate_attribute_slugs()

    def _generate_attribute_slugs(self):
        for attr in self.attributes:
            if not getattr(attr, 'slug', None):
                attr["slug"] = slugify(attr["name"])

    @before_event(Delete)
    async def on_delete(self):
        from app.models.product import Product
        await Product.find(Product.category.id == self.id).delete()
