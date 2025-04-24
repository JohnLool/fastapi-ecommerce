from typing import List, Any, Optional

from app.models.product import Product
from app.repositories.mongo_repos.category_repo import CategoryRepository
from app.repositories.mongo_repos.product_repo import ProductRepository
from app.schemas.product import ProductOut, ProductCreate
from app.services.base_service import BaseService
from app.utils.logger import logger


class ProductService(BaseService[ProductRepository]):
    def __init__(self, repo: ProductRepository = ProductRepository()):
        super().__init__(repo, ProductOut)
        self.category_repo = CategoryRepository()

    async def get_by_slug(self, slug: str) -> ProductOut:
        product = await self.repository.get_by_slug(slug)
        if not product:
            logger.warning(f"Service: Product with slug {slug} not found")
            return None
        await product.fetch_link(Product.category)
        product_dict = product.model_dump(by_alias=True)
        product_dict["category"] = product.category.slug
        return ProductOut.model_validate(product_dict)

    async def get_all(self, *filters: Any) -> List[ProductOut]:
        logger.info(f"ProductService: Getting all products")
        products = await self.repository.get_all(*filters)
        results: List[ProductOut] = []
        for product in products:
            if product.category:
                await product.fetch_link(Product.category)
                category_slug = product.category.slug
            else:
                category_slug = None
            product_dict = product.model_dump(by_alias=True)
            product_dict["category"] = category_slug
            results.append(ProductOut.model_validate(product_dict))
        return results

    async def create(self, data: ProductCreate) -> Optional[ProductOut]:
        product_dict = data.model_dump(exclude_unset=True)
        slug_category = product_dict.pop("category", None)
        if slug_category:
            category = await self.category_repo.get_by_field("slug", slug_category)
            if not category:
                return None
            product_dict["category"] = category

        product = await self.repository.create(product_dict)
        if not product:
            return None

        await product.fetch_link(Product.category)
        product_dict_out = product.model_dump(by_alias=True)
        product_dict_out["category"] = product.category.slug
        return ProductOut.model_validate(product_dict_out)