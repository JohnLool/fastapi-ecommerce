from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=255)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=5, max_length=16)


class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    username: str = Field(None, min_length=5, max_length=255)
    email: EmailStr | None = None
    password: str = Field(None, min_length=5, max_length=16)