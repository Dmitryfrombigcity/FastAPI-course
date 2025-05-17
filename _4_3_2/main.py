# main
# see https://github.com/laurentS/slowapi/issues/13

from typing import Any, Annotated, Callable, Awaitable

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from starlette.responses import Response

from _4_3_2.authentication import create_access_token, create_refresh_token
from _4_3_2.dependencies import authenticate_user, get_user_by_token
from _4_3_2.protected_resource import request_ctx_var, limiter, router, get_rate_limit_by_role
from _4_3_2.rbac import PermissionChecker
from _4_3_2.schemas import User
from _4_3_2.users import refresh_tokens

http_bearer = HTTPBearer(auto_error=False)  # for test purpose only

app = FastAPI(dependencies=[Depends(http_bearer)])
app.include_router(router)


@app.middleware("http")
async def request_context_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_ctx = request_ctx_var.set(request)
    response = await call_next(request)
    request_ctx_var.reset(request_ctx)
    return response


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def _helper(username: str) -> tuple[str, str]:
    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)
    refresh_tokens[username] = refresh_token
    return access_token, refresh_token


@app.post(
    "/login/",
    dependencies=[Depends(authenticate_user)],
    tags=["Sign-in"]
)
async def sign_in(user: User) -> Any:
    access_token, refresh_token = _helper(user.username)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@app.post(
    "/refresh/",
    tags=["Refresh tokens"]
)
async def update_tokens(
        username: Annotated[str, Depends(get_user_by_token)]
) -> Any:
    access_token, refresh_token = _helper(username)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@app.get(
    "/admin/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin"]))
    ],
    tags=["Users"]
)
@limiter.limit(get_rate_limit_by_role)
async def get_admin_resource(request: Request) -> Any:
    return {"message": "Access granted"}


@app.get(
    "/user/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user"]))
    ],
    tags=["Users"]
)
@limiter.limit(get_rate_limit_by_role)
async def get_users_resource(request: Request) -> Any:
    return {"message": "Access granted"}


@app.get(
    "/guest/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user", "guest"]))
    ],
    tags=["Users"]
)
@limiter.limit(get_rate_limit_by_role)
async def get_guests_resource(request: Request) -> Any:
    return {"message": "Access granted"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
