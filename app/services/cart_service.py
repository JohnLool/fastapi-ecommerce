from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.services.base_service import BaseService
from app.repositories.cart_repo import CartRepository
from app.repositories.cart_item_repo import CartItemRepository
from app.schemas.cart import CartOut, CartItemOut
from app.models.cart_item import CartItemOrm
from app.models.cart import CartOrm


class CartService(BaseService[CartRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(CartRepository(db), CartOut)
        self.item_repo = CartItemRepository(db)

    async def add_item(
        self,
        user_id: int,
        product_snapshot: dict,
        quantity: int = 1
    ) -> CartItemOut:
        cart: CartOrm = await self.repository.get_or_create_by_user(user_id)

        existing = await self.item_repo.get_for_cart_and_product(
            cart.id, product_snapshot["id"]
        )

        if existing:
            new_qty = existing.quantity + quantity
            updated = await self.item_repo.update(existing.id, {"quantity": new_qty})
            if not updated:
                return None

            return CartItemOut.model_validate(updated)

        data = {
            "cart_id": cart.id,
            "product_id": product_snapshot["id"],
            "quantity": quantity,
            "title_snapshot": product_snapshot["name"],
            "price_snapshot": product_snapshot["price"],
            "image_snapshot": product_snapshot.get("image_url"),
        }
        created = await self.item_repo.create(data)
        if not created:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to create cart item")
        return CartItemOut.model_validate(created)

    async def get_cart(self, user_id: int) -> CartOut:
        # Берём корзину; если нет — создаём пустую
        cart = await self.repository.get_by_user_id(user_id)
        if not cart:
            cart = await self.repository.create({"user_id": user_id})
        # ORM → Pydantic
        return CartOut.model_validate(cart)

    async def remove_item(self, item_id: int) -> CartItemOut:
        # Удаляем айтем (soft-delete или hard-delete по твоей реализации)
        removed = await self.item_repo.delete(item_id)
        if not removed:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        return CartItemOut.model_validate(removed)

    async def clear_cart(self, user_id: int) -> CartOut:
        # Удаляем все айтемы корзины
        cart = await self.repository.get_by_user_id(user_id)
        if not cart:
            return CartOut.model_validate(cart)
        for item in list(cart.items):
            await self.item_repo.delete(item.id)
        # Обновляем корзину
        cart = await self.repository.get_by_user_id(user_id)
        return CartOut.model_validate(cart)
