from contextlib import asynccontextmanager
from typing import AsyncIterator, Annotated, Any

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis import asyncio as redis
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from _4_3_3.api.endpoints.auth.dependencies import get_current_user
from _4_3_3.schemas import UserSchema

http_bearer = HTTPBearer(auto_error=False)  # for test purpose only


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


async def get_rate_limit_by_role(
        request: Request,
        response: Response,
        user: Annotated[UserSchema, Depends(get_current_user)]
) -> Any:
    match user.role:
        case "admin":
            times = 50
        case "user":
            times = 20
        case "guest":
            times = 10
        case _:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    return await RateLimiter(times=times, minutes=1)(request, response)
