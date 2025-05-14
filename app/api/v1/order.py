from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import require_scopes
from app.dependencies.services import get_cart_service, get_order_service, get_product_service
from app.schemas.order import OrderCreate, OrderOut
from app.services.cart_service import CartService
from app.services.mongo_services.product_service import ProductService
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/checkout", response_model=OrderOut, status_code=201)
async def checkout(
    order_data: OrderCreate,
    current_user = Depends(require_scopes("create:order")),
    cart_service: CartService = Depends(get_cart_service),
    order_service: OrderService = Depends(get_order_service),
    prod_service: ProductService = Depends(get_product_service)
):
    cart = await cart_service.get_or_create_by_user(current_user.id)
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for ci in cart.items:
        product = await prod_service.check_stock(ci.product_slug, ci.quantity)
        if not product:
            raise HTTPException(status_code=400, detail="Not enough stock")

    order = await order_service.create_order(cart, order_data)
    if not order:
        raise HTTPException(status_code=500, detail="Order creation failed")
    await cart_service.clear_cart(current_user.id)
    return order
