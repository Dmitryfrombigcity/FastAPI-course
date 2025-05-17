from typing import Any, Annotated

from fastapi import Depends, APIRouter

from _4_3_3.api.endpoints.auth.authentication import create_access_token, create_refresh_token
from _4_3_3.api.endpoints.auth.dependencies import authenticate_user, get_user_by_token
from _4_3_3.schemas import User
from _4_3_3.users import refresh_tokens

router = APIRouter()


def _helper(username: str) -> tuple[str, str]:
    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)
    refresh_tokens[username] = refresh_token
    return access_token, refresh_token


@router.post(
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


@router.post(
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
