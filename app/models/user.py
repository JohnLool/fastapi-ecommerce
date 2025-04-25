from enum import Enum

from app.core.database import Base
from sqlalchemy import String, Boolean, Integer, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Role(str, Enum):
    owner        = "owner"        # site owner, all rights, can create new categories
    admin        = "admin"        # site operator, can help sellers/customers
    seller       = "seller"       # can create/edit/delete products
    customer     = "customer"     # can buy, remain active


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    role: Mapped[Role] = mapped_column(
        SqlEnum(Role, name="role_enum"),
        server_default=Role.customer,
        nullable=False
    )