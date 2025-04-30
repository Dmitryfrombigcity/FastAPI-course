# main.py

import secrets
from functools import lru_cache
from typing import Annotated, Any

import bcrypt
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from _4_1_3 import config
from _4_1_3.config import Settings
from _4_1_3.schemas import User, UserInDB

fake_users_db: list[UserInDB] = []


@lru_cache
def get_settings() -> Settings:
    return config.Settings()


app = FastAPI(redoc_url=None, docs_url=None, openapi_url=None)
security = HTTPBasic()


def hide_doc() -> None:
    if get_settings().MODE == 'PROD':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND)


def auth_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    for item in fake_users_db:
        if credentials.username == item.username \
                and bcrypt.checkpw(
                    credentials.password.encode(), item.hashed_password.encode()
                ):
            return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"}
    )


def auth_doc(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> dict[str, str]:
    if secrets.compare_digest(credentials.username, get_settings().DOCS_USER) \
            and secrets.compare_digest(
                credentials.password, get_settings().DOCS_PASSWORD.get_secret_value()
            ):
        return {"message": "Access granted"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"}
    )


@app.post("/register/")
async def sign_up(user: User) -> Any:
    for item in fake_users_db:
        if user.username == item.username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User already exists")
    fake_users_db.append(
        UserInDB(
            username=user.username,
            hashed_password=bcrypt.hashpw(
                user.password.encode(), bcrypt.gensalt()).decode()))
    return {"message": f"{user.username} was successfully added"}


@app.get("/login/")
async def sign_in(username: Annotated[str, Depends(auth_user)]) -> Any:
    return {"message": f"Welcome, {username}!"}


@app.get(
    "/docs",
    include_in_schema=False,
    dependencies=[
        Depends(hide_doc), Depends(auth_doc)
    ]
)
async def docs_html() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get(
    "/openapi.json",
    include_in_schema=False,
    dependencies=[
        Depends(hide_doc), Depends(auth_doc)
    ]
)
async def openapi_json() -> dict[str, Any]:
    return get_openapi(title="FastAPI", version="0.1.0", routes=app.routes)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
