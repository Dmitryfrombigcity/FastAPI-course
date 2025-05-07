# dependencies

from typing import Annotated

from fastapi import HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette import status
from starlette.requests import Request

from _4_2_3.authentication import decode_jwt
from _4_2_3.schemas import User
from _4_2_3.users import users_db, refresh_tokens
from _4_2_3.validation import validate_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
limiter = Limiter(key_func=get_remote_address)


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


unauth_err = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid token error",
    headers={"WWW-Authenticate": "Bearer"}
)


def is_valid_token(token: Annotated[str, Depends(oauth2_scheme)]) -> None:
    try:
        payload = decode_jwt(token=token)
        if payload.get("type") != "access":
            raise unauth_err
    except InvalidTokenError:
        raise unauth_err


async def get_user_by_token(token: Annotated[str, Body()]) -> str:
    try:
        payload = decode_jwt(token=token)
        if payload.get("type") != "refresh" \
                or (token != refresh_tokens.get(payload["sub"])):
            raise unauth_err
        return payload["sub"]
    except InvalidTokenError:
        raise unauth_err
