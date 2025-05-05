from authx import RequestToken, TokenPayload
from authx.exceptions import AuthXException
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.authx_security import security
from app.dependecies.services import get_user_service
from app.models.user import UserOrm, Role
from app.services.user_service import UserService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login",
)


ADDITIONAL_SCOPES: dict[Role, list[str]] = {
    Role.customer: [
        "read:products",
        "read:orders",
        "read:profile",
        "create:role_request",
    ],
    Role.seller: [
        "create:product",
        "update:product",
        "delete:product",
        "create:shop",
        "update:shop",
        "delete:shop",
    ],
    Role.admin: [
        "ban:user",
        "update:role"
    ],
    Role.owner: [
        "*",
        "create:category",
        "update:category",
        "delete:category",
    ],
}


ORDERED_ROLES: list[Role] = [
    Role.customer,
    Role.seller,
    Role.admin,
    Role.owner,
]


def get_scopes_for_role(role: Role) -> list[str]:
    scopes: list[str] = []
    for r in ORDERED_ROLES:
        for s in ADDITIONAL_SCOPES.get(r, []):
            if s not in scopes:
                scopes.append(s)
        if r == role:
            break
    return scopes

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token processing error",
        )

async def get_current_user(
    user_service: UserService = Depends(get_user_service),
    payload: TokenPayload     = Depends(get_payload),
) -> UserOrm:
    user = await user_service.get_by_username_orm(payload.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

def require_scopes(*required: str):
    async def checker(
        payload: TokenPayload  = Depends(get_payload),
        current_user: UserOrm  = Depends(get_current_user),
    ):
        token_scopes = payload.scopes or []
        if "*" in token_scopes:
            return current_user
        for scope in required:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not enough permissions",
                )
        return current_user
    return checker
