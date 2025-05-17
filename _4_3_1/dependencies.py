# dependencies

from typing import Annotated

from fastapi import HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status
from starlette.requests import Request

from _4_3_1.authentication import decode_jwt
from _4_3_1.schemas import User, UserSchema
from _4_3_1.users import users_db, refresh_tokens
from _4_3_1.validation import validate_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


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
    detail="Invalid token error",
    headers={"WWW-Authenticate": "Bearer"}
)


async def check_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = decode_jwt(token=token)
        if payload.get("type") != "access":
            raise unauth_err
    except InvalidTokenError:
        raise unauth_err
    assert (username := payload.get("sub"))
    return username


async def get_current_user(current_user: Annotated[str, Depends(check_token)]) -> UserSchema:
    assert (user := users_db.get(current_user))
    return user


async def get_user_by_token(token: Annotated[str, Body()]) -> str:
    try:
        payload = decode_jwt(token=token)
        if payload.get("type") != "refresh" \
                or (token != refresh_tokens.get(payload["sub"])):
            raise unauth_err
        return payload["sub"]
    except InvalidTokenError:
        raise unauth_err
