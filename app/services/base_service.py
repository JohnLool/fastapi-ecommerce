from typing import List, Optional, Type, TypeVar, Generic, Any
from pydantic import BaseModel
from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger

Repository = TypeVar("Repository", bound=BaseRepository)
SchemaOut = TypeVar("SchemaOut", bound=BaseModel)
SchemaBase = TypeVar("SchemaBase", bound=BaseModel)


class BaseService(Generic[Repository]):
    def __init__(self, repository: Repository, schema_out: Type[SchemaOut]):
        self.repository = repository
        self.schema_out = schema_out

    async def create(self, data: SchemaBase) -> Optional[SchemaOut]:
        data_dict = data.model_dump() if hasattr(data, "model_dump") else data
        logger.info(f"Service: Creating {self.repository.model.__name__} with data: {data_dict}")
        record = await self.repository.create(data_dict)
        if not record:
            logger.error("Service: Creation failed.")
            return None
        record = await self.repository.get_by_id(record.id)
        if not record:
            logger.error("Service: Failed to retrieve created record.")
            return None
        record_dict = record.model_dump(by_alias=True)
        return self.schema_out.model_validate(record_dict)

    async def update(self, record_id: Any, data: SchemaBase) -> Optional[SchemaOut]:
        data_dict = data.model_dump() if hasattr(data, "model_dump") else data
        logger.info(f"Service: Updating {self.repository.model.__name__} with id {record_id} using data: {data_dict}")
        record = await self.repository.update(record_id, data_dict)
        if not record:
            logger.error(f"Service: Update failed for id {record_id}")
            return None
        record_dict = record.model_dump(by_alias=True)
        return self.schema_out.model_validate(record_dict)

    async def delete(self, record_id: Any) -> Optional[SchemaOut]:
        logger.info(f"Service: Deleting {self.repository.model.__name__} with id {record_id}")
        record = await self.repository.delete(record_id)
        if not record:
            logger.error(f"Service: Delete failed for id {record_id}")
            return None
        record_dict = record.model_dump(by_alias=True)
        return self.schema_out.model_validate(record_dict)

    async def get_all(self, *filters: Any) -> List[SchemaOut]:
        logger.info(f"Service: Getting all {self.repository.model.__name__}")
        records = await self.repository.get_all(*filters)
        results: List[SchemaOut] = []
        for rec in records:
            rec_dict = rec.model_dump(by_alias=True)
            results.append(self.schema_out.model_validate(rec_dict))
        return results

    async def get_by_id(self, record_id: Any) -> Optional[SchemaOut]:
        logger.info(f"Service: Getting {self.repository.model.__name__} by id {record_id}")
        record = await self.repository.get_by_id(record_id)
        if not record:
            logger.warning(f"Service: Record with id {record_id} not found")
            return None
        record_dict = record.model_dump(by_alias=True)
        return self.schema_out.model_validate(record_dict)