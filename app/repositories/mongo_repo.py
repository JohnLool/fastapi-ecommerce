from typing import TypeVar, Generic, List, Optional, Any

from beanie import Document
from app.repositories.abstract_repo import AbstractRepository

T = TypeVar("T", bound=Document)

class MongoRepository(AbstractRepository[T], Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    async def get_by_field(self, field: str, value: Any) -> Optional[T]:
        query = {field: value}
        return await self.model.find_one(query)

    async def get_all(self, *filters: Any) -> List[T]:
        cursor = self.model.find(*filters)
        return await cursor.to_list()

    async def create(self, item_data: dict) -> Optional[T]:
        instance = self.model(**item_data)
        inserted = await instance.insert()
        return inserted

    async def update(self, item_id: Any, item_data: dict) -> Optional[T]:
        doc = await self.model.get(item_id)
        if not doc:
            return None
        for key, val in item_data.items():
            setattr(doc, key, val)
        await doc.save()
        return doc

    async def delete(self, item_id: Any) -> Optional[T]:
        doc = await self.model.get(item_id)
        if not doc:
            return None
        await doc.delete()
        return doc
