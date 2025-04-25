from authx import RequestToken, TokenPayload
from authx.exceptions import AuthXException
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.authx_security import security
from app.dependecies.services import get_user_service
from app.models.user import Role, UserOrm
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_payload(
    token: str = Depends(oauth2_scheme),
) -> TokenPayload:
    try:
        req = RequestToken(
            token=token,
            type="access",
            location="headers",
            csrf=None,
        )
        payload = security.verify_token(req)
        return payload
    except AuthXException as e:
        print(f"AuthX error: {e}")
        raise HTTPException(401, "Invalid or expired token")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(401, "Token processing error")

async def get_current_user(
        user_service: UserService = Depends(get_user_service),
        payload: TokenPayload = Depends(get_payload),
) -> UserOrm:
    user = await user_service.get_by_username_orm(payload.sub)
    if not user:
        raise HTTPException(404, "User not found")
    return user

def require_role(*allowed_roles: Role):
    async def checker(
        current_user: UserOrm = Depends(get_current_user),
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(403, "Not enough permissions")
        return current_user
    return checker