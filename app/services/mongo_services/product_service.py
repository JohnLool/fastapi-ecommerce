from typing import List, Any, Optional
from uuid import uuid4

from bson import Decimal128
from slugify import slugify

from app.exceptions import WrongTypeError, UnexpectedAttributeError, MissingAttributeError
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

    @staticmethod
    async def validate_product_attributes(product: Product) -> None:
        if not product.category:
            return

        await product.fetch_link(Product.category)
        cat = product.category
        defs = cat.attributes
        defs_map = {d.slug: d for d in defs}

        for d in defs:
            if d.required and d.slug not in product.attributes:
                raise MissingAttributeError(d.slug)

        for key in product.attributes:
            if key not in defs_map:
                raise UnexpectedAttributeError(key)

        for slug, value in product.attributes.items():
            expected = defs_map[slug].type
            if expected == "int" and not isinstance(value, int):
                raise WrongTypeError(slug, "int")
            if expected == "float" and not isinstance(value, float):
                raise WrongTypeError(slug, "float")
            if expected == "bool" and not isinstance(value, bool):
                raise WrongTypeError(slug, "bool")
            if expected == "str" and not isinstance(value, str):
                raise WrongTypeError(slug, "str")

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

        temp = Product(**product_dict)
        await self.validate_product_attributes(temp)

        product = await self.repository.create(product_dict)
        if not product:
            return None

        await product.fetch_link(Product.category)
        product_dict_out = product.model_dump(by_alias=True)
        product_dict_out["category"] = product.category.slug
        return ProductOut.model_validate(product_dict_out)

    async def update(self, item_id: Any, data: ProductUpdate) -> Optional[ProductOut]:
        product_dict = data.model_dump(exclude_unset=True)

        existing = await self.repository.get_by_id(item_id)
        if not existing:
            return None

        if "category" in product_dict:
            slug_category = product_dict.pop("category")
            if slug_category:
                category = await self.category_repo.get_by_field("slug", slug_category)
                if not category:
                    return None
                product_dict["category"] = category

        if "name" in product_dict and product_dict["name"] != existing.name:
            base = slugify(product_dict["name"])
            suf = uuid4().hex[:8]
            product_dict["slug"] = f"{base}-{suf}"

        for k, v in product_dict.items():
            setattr(existing, k, v)
        await self.validate_product_attributes(existing)

        product = await self.repository.update(item_id, product_dict)
        if not product:
            return None

        await product.fetch_link(Product.category)
        product_dict_out = product.model_dump(by_alias=True)
        product_dict_out["category"] = product.category.slug if product.category else None
        return ProductOut.model_validate(product_dict_out)
