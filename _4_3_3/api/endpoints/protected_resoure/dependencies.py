from typing import Annotated

from fastapi import Path, Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request

from _4_3_3.api.endpoints.auth.dependencies import get_current_user
from _4_3_3.schemas import UserSchema
from _4_3_3.users import resources


async def check_permission(
        request: Request,
        username: Annotated[str, Path()],
        user: Annotated[UserSchema, Depends(get_current_user)]

) -> None:
    if username not in resources.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    match request.method:
        case "GET":
            is_public = resources.get(username).get("is_public")  # type:ignore
            if user.username in (username, "admin") or is_public:
                return
        case "POST" | "PUT" | "DELETE":
            if user.username in (username, "admin"):
                return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access forbidden"
    )
