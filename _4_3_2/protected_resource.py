# protected_resource

from contextvars import ContextVar
from typing import Any

from fastapi import Depends, APIRouter
from jwt import InvalidTokenError
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from _4_3_2.authentication import decode_jwt
from _4_3_2.dependencies import unauth_err
from _4_3_2.rbac import PermissionChecker
from _4_3_2.users import users_db

request_ctx_var: ContextVar[Request | None] = ContextVar("request_ctx_var", default=None)

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/protected_resource")


def get_rate_limit_by_role() -> str:
    request = request_ctx_var.get()
    assert request
    authorization = request.headers.get("Authorization")
    assert authorization
    scheme, _, token = authorization.partition(" ")

    try:
        payload = decode_jwt(token=token)
        if payload.get("type") != "access":
            raise unauth_err
    except InvalidTokenError:
        raise unauth_err
    user = users_db.get(payload.get("sub"))
    assert user

    limit: str = ""
    match user.role:
        case "admin":
            limit = "10/minute"
        case "user":
            limit = "2/minute"
        case "guest":
            limit = "1/minute"
    return limit


@router.get(
    "/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user"]))
    ],
    tags=["Fetch protected resource"]
)
@limiter.limit(get_rate_limit_by_role)
async def get_protected_resource(request: Request) -> Any:
    return {"message": "Access granted"}
