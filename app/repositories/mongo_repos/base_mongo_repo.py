from typing import TypeVar, Generic, List, Optional, Any

from beanie import Document
from app.repositories.abstract_repo import AbstractRepository


T = TypeVar("T", bound=Document)


class BaseMongoRepository(AbstractRepository[T], Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    async def get_by_field(self, field: str, value: Any) -> Optional[T]:
        return await self.model.find_one({field: value})

    async def get_by_id(self, item_id: Any) -> Optional[T]:
        return await self.model.get(item_id)

    async def get_by_slug(self, slug: str) -> Optional[T]:
        return await self.model.find_one({"slug": slug})

    async def get_all(self, *filters: Any) -> List[T]:
        query = self.model.find(*filters) if filters else self.model.find()
        return await query.to_list()

    async def create(self, item_data: dict) -> Optional[T]:
        instance = self.model(**item_data)
        return await instance.create()

    async def update(self, item_id: Any, item_data: dict) -> Optional[T]:
        doc = await self.model.get(item_id)
        if not doc:
            return None
        for key, val in item_data.items():
            setattr(doc, key, val)
        await doc.replace()
        return doc

    async def delete(self, item_id: Any) -> Optional[T]:
        doc = await self.model.get(item_id)
        if not doc:
            return None
        await doc.delete()
        return doc
