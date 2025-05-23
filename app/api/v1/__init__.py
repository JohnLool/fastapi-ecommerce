from fastapi import APIRouter
from . import products, categories, shops, users, role_requests, cart, order

router = APIRouter(prefix="/api/v1")
router.include_router(products.router)
router.include_router(categories.router)
router.include_router(shops.router)
router.include_router(users.router)
router.include_router(role_requests.router)
router.include_router(cart.router)
router.include_router(order.router)