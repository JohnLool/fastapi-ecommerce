from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, func, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ShopOrm(Base):
    __tablename__ = 'shops'
    __table_args__ = (
        Index("uq_shops_name_active", "name", unique=True, postgresql_where="deleted = false"),
        Index("uq_shops_slug_active", "slug", unique=True, postgresql_where="deleted = false"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, default='', nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())
    deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    owner: Mapped["UserOrm"] = relationship("UserOrm", back_populates='shops')