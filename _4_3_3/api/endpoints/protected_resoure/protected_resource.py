from typing import Any

from fastapi import Depends, APIRouter

from _4_3_3.api.endpoints.protected_resoure.dependencies import check_permission
from _4_3_3.rbac import PermissionChecker
from _4_3_3.util import get_rate_limit_by_role

router = APIRouter(prefix="/protected_resource")


@router.get(
    "/{username}/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user", "guest"])),
        Depends(get_rate_limit_by_role),
        Depends(check_permission)
    ],
    tags=["Fetch protected resource"]
)
async def get_protected_resource() -> Any:
    return {"message": "Access granted"}


@router.post(
    "/{username}/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user"])),
        Depends(get_rate_limit_by_role),
        Depends(check_permission)
    ],
    tags=["Create protected resource"]
)
async def create_protected_resource() -> Any:
    return {"message": "Access granted"}


@router.put(
    "/{username}/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user"])),
        Depends(get_rate_limit_by_role),
        Depends(check_permission)
    ],
    tags=["Update protected resource"]
)
async def update_protected_resource() -> Any:
    return {"message": "Access granted"}


@router.delete(
    "/{username}/",
    dependencies=[
        Depends(PermissionChecker(roles=["admin", "user"])),
        Depends(get_rate_limit_by_role),
        Depends(check_permission)
    ],
    tags=["Delete protected resource"]
)
async def delete_protected_resource() -> Any:
    return {"message": "Access granted"}
