from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import OrderOrm, OrderItemOrm
from app.repositories.order_repo import OrderRepository
from app.schemas.cart import CartOut

from app.schemas.order import OrderOut, OrderCreate

from app.services.base_service import BaseService


class OrderService(BaseService[OrderRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(OrderRepository(db), OrderOut)

    async def create_order(
        self,
        cart: CartOut,
        order_data: OrderCreate
    ) -> OrderOut:
        if not cart.items:
            return None

        items_payload = [
            {
                "product_slug": item.product_slug,
                "quantity":      item.quantity,
                "title_snapshot": item.title_snapshot,
                "price_snapshot": item.price_snapshot,
                "image_snapshot": item.image_snapshot,
            }
            for item in cart.items
        ]

        subtotal      = sum(item.price_snapshot * item.quantity for item in cart.items)
        discount_total= Decimal("0.00")
        delivery_fee  = Decimal("0.00")
        grand_total   = subtotal - discount_total + delivery_fee

        order_orm = await self.repository.create_order_with_items(
            user_id=cart.user_id,
            shipping_address=order_data.shipping_address,
            payment_method=order_data.payment_method,
            items_payload=items_payload,
            subtotal=subtotal,
            discount_total=discount_total,
            delivery_fee=delivery_fee,
            grand_total=grand_total,
        )
        return OrderOut.model_validate(order_orm)