from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class CartItemOrm(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"))
    product_slug: Mapped[str]
    quantity: Mapped[int] = mapped_column(default=1)

    title_snapshot: Mapped[str]
    price_snapshot: Mapped[float]
    image_snapshot: Mapped[str | None] = mapped_column(nullable=True)

    cart: Mapped["CartOrm"] = relationship("CartOrm", back_populates="items")
