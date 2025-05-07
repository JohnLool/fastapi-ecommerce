from __future__ import annotations

from sqlalchemy import ForeignKey, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base


class CartOrm(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    items: Mapped[list["CartItemOrm"]] = relationship(
        "CartItemOrm",
        back_populates="cart",
        cascade="all, delete-orphan"
    )
