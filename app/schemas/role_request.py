from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.user import Role
from app.models.role_request import RequestStatus


class RoleRequestCreate(BaseModel):
    desired_role: Role = "seller"

class RoleRequestOut(BaseModel):
    id: int
    user_id: int
    desired_role: Role
    status: RequestStatus
    created_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )