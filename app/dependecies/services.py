from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.services.user_service import UserService


async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_session)],
) -> UserService:
    return UserService(db)