from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.product import ProductOut
from app.services.base_service import BaseService
from app.repositories.cart_repo import CartRepository
from app.repositories.cart_item_repo import CartItemRepository
from app.schemas.cart import CartOut, CartItemOut


class CartService(BaseService[CartRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(CartRepository(db), CartOut)
        self.item_repo = CartItemRepository(db)

    async def add_item(
        self,
        user_id: int,
        product: ProductOut,
        quantity: int = 1
    ) -> Optional[CartItemOut]:
        cart = await self.repository.get_or_create_by_user(user_id)

        existing = await self.item_repo.get_for_cart_and_slug(cart.id, product.slug)
        if existing:
            new_qty = existing.quantity + quantity
            updated = await self.item_repo.update(existing.id, {"quantity": new_qty})
            if not updated:
                return None
            return CartItemOut.model_validate(updated)

        data = {
            "cart_id":        cart.id,
            "product_slug":   product.slug,
            "quantity":       quantity,
            "title_snapshot": product.name,
            "price_snapshot": product.price,
            "image_snapshot": product.image_url,
        }
        created = await self.item_repo.create(data)
        if not created:
            return None
        return CartItemOut.model_validate(created)

    async def get_or_create_by_user(self, user_id: int) -> CartOut:
        cart = await self.repository.get_or_create_by_user(user_id)
        return CartOut.model_validate(cart)

    async def update_item(self, item_id: int, quantity: int) -> CartItemOut:
        updated = await self.item_repo.update(item_id, {"quantity": quantity})
        if not updated:
            return None
        return CartItemOut.model_validate(updated)

    async def remove_item(self, item_id: int) -> Optional[CartItemOut]:
        removed = await self.item_repo.delete(item_id)
        if not removed:
            return None
        return CartItemOut.model_validate(removed)

    async def clear_cart(self, user_id: int) -> Optional[CartOut]:
        cart = await self.repository.get_by_user_id(user_id)
        if not cart:
            return None

        for item in list(cart.items):
            await self.item_repo.delete(item.id)

        cart = await self.repository.get_by_user_id(user_id)
        return CartOut.model_validate(cart)
