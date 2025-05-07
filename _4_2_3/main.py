# main.py
from typing import Any, Annotated

import uvicorn
from fastapi import FastAPI, status, Depends
from fastapi.security import HTTPBearer
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from _4_2_3.authentication import create_access_token, create_refresh_token
from _4_2_3.dependencies import limiter, check_user, authenticate_user, is_valid_token, get_user_by_token
from _4_2_3.schemas import User, UserSchema
from _4_2_3.users import users_db, refresh_tokens
from _4_2_3.validation import hash_password

http_bearer = HTTPBearer(auto_error=False)  # for test purpose only

app = FastAPI(dependencies=[Depends(http_bearer)])

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def _helper(username: str) -> tuple[str, str]:
    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)
    refresh_tokens[username] = refresh_token
    return access_token, refresh_token


@app.post(
    "/register/",
    dependencies=[Depends(check_user)],
    status_code=status.HTTP_201_CREATED,
    tags=["Sign-up"]
)
async def sign_up(user: User) -> Any:
    users_db[user.username] = UserSchema(
        username=user.username,
        password=hash_password(user.password)
    )
    return {"message": "New user created"}


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
    dependencies=[Depends(is_valid_token)],
    tags=["Fetch protected resource"]
)
async def get_resource() -> Any:
    return {"message": "Access granted"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
