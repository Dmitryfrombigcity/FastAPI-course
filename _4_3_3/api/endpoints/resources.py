from typing import Any

from fastapi import Depends, APIRouter

from _4_3_3.util import get_rate_limit_by_role
from _4_3_3.rbac import PermissionChecker

router = APIRouter()


@router.get(
    "/admin/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin"])),
        Depends(get_rate_limit_by_role)
    ],
    tags=["Users"]
)
async def get_admin_resource() -> Any:
    return {"message": "Access granted"}


@router.get(
    "/user/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user"])),
        Depends(get_rate_limit_by_role)
    ],
    tags=["Users"]
)
async def get_users_resource() -> Any:
    return {"message": "Access granted"}


@router.get(
    "/guest/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user", "guest"])),
        Depends(get_rate_limit_by_role)
    ],
    tags=["Users"]
)
async def get_guests_resource() -> Any:
    return {"message": "Access granted"}
