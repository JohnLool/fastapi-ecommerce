from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class Product(Document):
    name: str
    description: Optional[str]
    price: float
    in_stock: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "products"
