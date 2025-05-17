# rbac

from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from _4_3_1.dependencies import get_current_user
from _4_3_1.schemas import UserSchema


class PermissionChecker:
    def __init__(self, roles: list[str]) -> None:
        self.roles = roles

    def __call__(self, user: Annotated[UserSchema, Depends(get_current_user)]) -> None:
        if user.role not in self.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden"
            )
