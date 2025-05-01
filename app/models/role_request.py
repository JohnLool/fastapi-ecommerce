from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, Enum as SqlEnum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.user import Role, UserOrm


class RequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class RoleRequestOrm(Base):
    __tablename__ = "role_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    desired_role: Mapped[Role] = mapped_column(SqlEnum(Role, name="role_enum"), nullable=False)
    status: Mapped[RequestStatus] = mapped_column(SqlEnum(RequestStatus), default=RequestStatus.pending, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    processed_at: Mapped[datetime | None] = mapped_column(onupdate=func.now(), nullable=True)

    user: Mapped[UserOrm] = relationship("UserOrm", back_populates="role_requests")
