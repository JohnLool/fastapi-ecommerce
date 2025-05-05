from fastapi import APIRouter
from . import products, categories, shops, users, role_requests

router = APIRouter(prefix="/api/v1")
router.include_router(products.router)
router.include_router(categories.router)
router.include_router(shops.router)
router.include_router(users.router)
router.include_router(role_requests.router)
