from app.repositories.mongo_repos.category_repo import CategoryRepository
from app.schemas.category import CategoryOut
from app.services.base_service import BaseService


class CategoryService(BaseService[CategoryRepository]):
    def __init__(self, repo: CategoryRepository = CategoryRepository()):
        super().__init__(repo, CategoryOut)