# main.py
from typing import Any, Annotated

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer

from _4_3_1.authentication import create_access_token, create_refresh_token
from _4_3_1.dependencies import authenticate_user, get_user_by_token
from _4_3_1.rbac import PermissionChecker
from _4_3_1.schemas import User
from _4_3_1.users import refresh_tokens

http_bearer = HTTPBearer(auto_error=False)  # for test purpose only

app = FastAPI(dependencies=[Depends(http_bearer)])


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
    "/protected_resource/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user"]))
    ],
    tags=["Fetch protected resource"]
)
async def get_protected_resource() -> Any:
    return {"message": "Access granted"}


@app.get(
    "/resource/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user", "guest"]))
    ],
    tags=["Read resource"]
)
async def get_resource() -> Any:
    return {"message": "Access granted"}


@app.post(
    "/resource/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin"]))
    ],
    tags=["Create resource"]
)
async def create_resource() -> Any:
    return {"message": "Access granted"}


@app.put(
    "/resource/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user"]))
    ],
    tags=["Update resource"]
)
async def update_resource() -> Any:
    return {"message": "Access granted"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
