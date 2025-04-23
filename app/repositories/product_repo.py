from app.models.product import Product
from app.repositories.base_mongo_repo import BaseMongoRepository


class ProductRepository(BaseMongoRepository[Product]):
    def __init__(self):
        super().__init__(Product)
