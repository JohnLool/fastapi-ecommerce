from __future__ import annotations
from enum import Enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Integer, String, ForeignKey, DateTime, Enum as SqlEnum,
    Numeric, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class OrderStatus(str, Enum):
    new = "new"
    paid = "paid"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    returned = "returned"


class OrderOrm(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    status: Mapped[OrderStatus] = mapped_column(
        SqlEnum(OrderStatus, name="order_status_enum"),
        nullable=False,
        server_default=OrderStatus.new
    )

    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    delivery_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    grand_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    payment_method: Mapped[str] = mapped_column(String(50), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(50), nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    shipping_address: Mapped[str] = mapped_column(String(1024), nullable=False)
    tracking_number: Mapped[str | None] = mapped_column(String(128), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

    items: Mapped[list["OrderItemOrm"]] = relationship(
        "OrderItemOrm",
        back_populates="order",
        cascade="all, delete-orphan"
    )