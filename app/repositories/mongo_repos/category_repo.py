from app.models.category import Category
from app.repositories.mongo_repos.base_mongo_repo import BaseMongoRepository


class CategoryRepository(BaseMongoRepository[Category]):
    def __init__(self):
        super().__init__(Category)