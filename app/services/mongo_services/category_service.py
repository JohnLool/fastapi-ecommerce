from app.repositories.mongo_repos.category_repo import CategoryRepository
from app.schemas.category import CategoryOut
from app.services.base_service import BaseService
from app.utils.logger import logger


class CategoryService(BaseService[CategoryRepository]):
    def __init__(self, repo: CategoryRepository = CategoryRepository()):
        super().__init__(repo, CategoryOut)

    async def get_by_slug(self, slug: str) -> CategoryOut:
        category = await self.repository.get_by_slug(slug)
        if not category:
            logger.warning(f"Service: Category with slug {slug} not found")
            return None
        category_dict = category.model_dump(by_alias=True)
        return CategoryOut.model_validate(category_dict)