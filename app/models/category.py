from beanie import Document, Indexed, before_event, Insert, PydanticObjectId, Replace
from pydantic import Field
from datetime import datetime, timezone
from slugify import slugify
from typing import Optional


class Category(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    name: Indexed(str, unique=True) = Field(...)
    slug: Indexed(str, unique=True) = Field(None)
    description: str = Field("")
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "categories"

    @before_event(Insert)
    def on_insert(self):
        now = datetime.now(timezone.utc)
        self.created_at = now
        self.updated_at = now
        self.slug = slugify(self.name)

    @before_event(Replace)
    def on_replace(self):
        self.updated_at = datetime.now(timezone.utc)
