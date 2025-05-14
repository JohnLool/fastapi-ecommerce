from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Security

from app.dependencies.validate_ownership import validate_item_in_cart_ownership
from app.models import CartItemOrm, UserOrm
from app.schemas.cart import CartOut, CartItemOut, AddCartItemIn, UpdateCartItem
from app.services.cart_service import CartService

from app.dependencies.services import get_cart_service, get_product_service
from app.dependencies.auth import require_scopes
from app.services.mongo_services.product_service import ProductService

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartOut)
async def get_or_create_cart(
    current_user: UserOrm = Depends(require_scopes("read:cart")),
    cart_service: CartService = Depends(get_cart_service),
):
    return await cart_service.get_or_create_by_user(current_user.id)

@router.post(
    "/items",
    response_model=CartItemOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_item(
    item_to_add: AddCartItemIn,
    current_user: UserOrm = Depends(require_scopes("add:cart_item")),
    cart_service: CartService = Depends(get_cart_service),
    prod_service: ProductService = Depends(get_product_service),
):
    product = await prod_service.get_by_slug(item_to_add.product_slug)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = await cart_service.add_item(current_user.id, product, item_to_add.quantity)
    if not cart_item:
        raise HTTPException(status_code=400, detail="Cart item creation failed")
    return cart_item

@router.patch(
    "/items/{item_id}",
    response_model=CartItemOut,
    dependencies=[Security(require_scopes("update:cart_item"))],
)
async def update_item(
    item_to_update: UpdateCartItem,
    item: CartItemOrm = Depends(validate_item_in_cart_ownership),
    cart_service: CartService = Depends(get_cart_service),
):
    updated = await cart_service.update_item(item.id, item_to_update.quantity)
    if not updated:
        raise HTTPException(status_code=400, detail="Update failed")
    return updated

@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_scopes("delete:cart_item"))],
)
async def remove_item(
    item: CartItemOrm = Depends(validate_item_in_cart_ownership),
    cart_service: CartService = Depends(get_cart_service),
):
    removed = await cart_service.remove_item(item.id)
    if not removed:
        raise HTTPException(status_code=400, detail="Deletion failed")

@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_cart(
    current_user: UserOrm = Depends(require_scopes("delete:cart")),
    cart_service: CartService = Depends(get_cart_service),
):
    return await cart_service.clear_cart(current_user.id)
