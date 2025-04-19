from authx import RequestToken
from authx.exceptions import AuthXException
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.authx_security import security
from app.dependecies.services import get_user_service
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(get_user_service),
):
    try:
        req = RequestToken(
            token=token,
            type="access",
            location="headers",
            csrf=None,
        )
        payload = security.verify_token(req)
        user = await user_service.get_by_username_orm(payload.sub)
        if not user:
            raise HTTPException(404, "User not found")
        return user
    except AuthXException as e:
        print(f"AuthX error: {e}")
        raise HTTPException(401, "Invalid or expired token")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(401, "Token processing error")