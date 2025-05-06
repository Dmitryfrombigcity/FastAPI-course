# main.py
from typing import Any, Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request

from _4_2_2.schemas import User, UserSchema
from _4_2_2.users import users_db
from _4_2_2.utils import create_access_token, validate_password, hash_password, decode_jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@limiter.limit("1/minute")
async def check_user(user: User, request: Request) -> None:
    if users_db.get(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )


@limiter.limit("5/minute")
async def authenticate_user(user: User, request: Request) -> None:
    if not (user_schema := users_db.get(user.username)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not validate_password(
            password=user.password,
            hashed_password=user_schema.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization failed"
        )


def is_valid_token(token: Annotated[str, Depends(oauth2_scheme)]) -> None:
    try:
        decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error",
            headers={"WWW-Authenticate": "Bearer"}
        )


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
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    "/protected_resource/",
    dependencies=[Depends(is_valid_token)],
    tags=["Fetch protected resource"]
)
async def get_resource() -> Any:
    return {"message": "Access granted"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
