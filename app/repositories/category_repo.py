from app.models.category import Category
from app.repositories.base_mongo_repo import BaseMongoRepository


class CategoryRepository(BaseMongoRepository[Category]):
    def __init__(self):
        super().__init__(Category)