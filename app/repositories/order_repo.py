from decimal import Decimal

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import OrderItemOrm
from app.repositories.base_repo import BaseRepository
from app.models.order import OrderOrm
from app.utils.logger import logger


class OrderRepository(BaseRepository[OrderOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(OrderOrm, session)

    async def create_order_with_items(
        self,
        user_id: int,
        shipping_address: str,
        payment_method: str | None,
        items_payload: list[dict],
        subtotal: Decimal,
        discount_total: Decimal,
        delivery_fee: Decimal,
        grand_total: Decimal,
    ) -> OrderOrm:
        order = OrderOrm(
            user_id=user_id,
            shipping_address=shipping_address,
            payment_method=payment_method,
            subtotal=subtotal,
            discount_total=discount_total,
            delivery_fee=delivery_fee,
            grand_total=grand_total,
        )

        order.items = [
            OrderItemOrm(**item_data)
            for item_data in items_payload
        ]

        try:
            self.session.add(order)
            await self.session.commit()
            await self.session.refresh(order, attribute_names=["items"])
            return order
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error in create_order_with_items: {e}")
            raise