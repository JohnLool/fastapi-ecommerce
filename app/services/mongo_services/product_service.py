from app.repositories.mongo_repos.product_repo import ProductRepository
from app.schemas.product import ProductOut
from app.services.base_service import BaseService


class ProductService(BaseService[ProductRepository]):
    def __init__(self, repo: ProductRepository = ProductRepository()):
        super().__init__(repo, ProductOut)