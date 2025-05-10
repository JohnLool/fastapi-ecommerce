from fastapi import Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.dependencies.repositories import get_cart_item_repo, get_cart_repo, get_product_repo, get_shop_repo
from app.models import UserOrm, ShopOrm, CartItemOrm
from app.models.product import Product
from app.repositories.cart_item_repo import CartItemRepository
from app.repositories.cart_repo import CartRepository

from app.repositories.mongo_repos.product_repo import ProductRepository
from app.repositories.shop_repo import ShopRepository


async def validate_shop_ownership(
    shop_slug: str,
    current_user: UserOrm = Depends(get_current_user),
    shop_repo: ShopRepository = Depends(get_shop_repo),
) -> ShopOrm:
    shop = await shop_repo.get_by_slug(shop_slug)
    if not shop:
        raise HTTPException(404, "Shop not found")
    if shop.owner_id != current_user.id:
        raise HTTPException(403, "Not enough permissions")
    return shop

async def validate_product_ownership(
    product_slug: str,
    current_user: UserOrm = Depends(get_current_user),
    prod_repo: ProductRepository = Depends(get_product_repo),
    shop_repo: ShopRepository = Depends(get_shop_repo),
) -> Product:
    product = await prod_repo.get_by_slug(product_slug)
    if not product:
        raise HTTPException(404, "Product not found")
    shop = await shop_repo.get_by_id(product.shop_id)
    if not shop or shop.owner_id != current_user.id:
        raise HTTPException(403, "Not enough permissions")
    return product

async def validate_item_in_cart_ownership(
    item_id: int,
    current_user: UserOrm = Depends(get_current_user),
    cart_item_repo: CartItemRepository = Depends(get_cart_item_repo),
    cart_repo: CartRepository = Depends(get_cart_repo),
) -> CartItemOrm:
    item = await cart_item_repo.get_by_id(item_id)
    if not item:
        raise HTTPException(404, "Cart item not found")
    cart = await cart_repo.get_by_id(item.cart_id)
    if not cart or cart.user_id != current_user.id:
        raise HTTPException(403, "Not enough permissions")
    return item