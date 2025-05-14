from typing import List, Any, Optional
from uuid import uuid4

from slugify import slugify

from app.models.product import Product
from app.repositories.mongo_repos.category_repo import CategoryRepository
from app.repositories.mongo_repos.product_repo import ProductRepository
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate
from app.services.base_service import BaseService
from app.utils.logger import logger


class ProductService(BaseService[ProductRepository]):
    def __init__(self, repo: ProductRepository = ProductRepository()):
        super().__init__(repo, ProductOut)
        self.category_repo = CategoryRepository()

    async def check_stock(self, slug: str, required_quantity: int) -> Optional[ProductOut]:
        product = await self.repository.get_by_slug(slug)
        if not product:
            return None
        if product.in_stock < required_quantity:
            return None
        return product

    async def get_by_slug(self, slug: str) -> Optional[ProductOut]:
        product = await self.repository.get_by_slug(slug)
        if not product:
            logger.warning(f"Service: Product with slug {slug} not found")
            return None
        await product.fetch_link(Product.category)
        product_dict = product.model_dump(by_alias=True)
        product_dict["category"] = product.category.slug
        product_dict["image_url"] = product.image_url
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

    async def create_with_shop(self, data: ProductCreate, shop_id: int) -> Optional[ProductOut]:
        product_dict = data.model_dump(exclude_unset=True)

        if "category" in product_dict:
            slug_category = product_dict.pop("category")
            if slug_category:
                category = await self.category_repo.get_by_field("slug", slug_category)
                if not category:
                    return None
                product_dict["category"] = category

        if "name" in product_dict:
            base = slugify(product_dict["name"])
            suf = uuid4().hex[:8]
            product_dict["slug"] = f"{base}-{suf}"

        product_dict["shop_id"] = shop_id

        product = await self.repository.create(product_dict)
        if not product:
            return None

        await product.fetch_link(Product.category)
        product_dict_out = product.model_dump(by_alias=True)
        product_dict_out["category"] = product.category.slug
        return ProductOut.model_validate(product_dict_out)

    async def update(self, item_id: Any, data: ProductUpdate) -> Optional[ProductOut]:
        product_dict = data.model_dump(exclude_unset=True)

        existing_product = await self.repository.get_by_id(item_id)
        if not existing_product:
            return None

        if "category" in product_dict:
            slug_category = product_dict.pop("category")
            if slug_category:
                category = await self.category_repo.get_by_field("slug", slug_category)
                if not category:
                    return None
                product_dict["category"] = category

        if "name" in product_dict and product_dict["name"] != existing_product.name:
            base = slugify(product_dict["name"])
            suf = uuid4().hex[:8]
            product_dict["slug"] = f"{base}-{suf}"

        product = await self.repository.update(item_id, product_dict)
        if not product:
            return None

        await product.fetch_link(Product.category)
        product_dict_out = product.model_dump(by_alias=True)
        product_dict_out["category"] = product.category.slug if product.category else None
        return ProductOut.model_validate(product_dict_out)
