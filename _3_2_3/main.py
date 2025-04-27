# main.py

import uuid
from typing import Annotated, Any

import uvicorn
from fastapi import FastAPI, Response, HTTPException, Body, Cookie
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired, BadData

from _3_2_3.config import settings
from _3_2_3.schemas import User, UserOut

MAX_AGE = 180

app = FastAPI()

db = [User(user="user123", password="password123")]


def set_cookie(
        token: str,
        response: Response
) -> None:
    response.set_cookie(
        key="session_token",
        value=token,
        secure=True,
        httponly=True,
        max_age=settings.max_age
    )


def generate_session_token(token_uuid: str) -> str:
    signer = TimestampSigner(secret_key=settings.secret.get_secret_value())
    token = f"{token_uuid}.{signer.get_timestamp()}"
    token_signed = signer.sign(token)
    return token_signed.decode()


def check_session_token(token: str) -> str:
    token_signed = token
    signer = TimestampSigner(secret_key=settings.secret.get_secret_value())
    try:
        signer.unsign(token, max_age=MAX_AGE)
    except SignatureExpired as err:
        assert err.payload
        token_uuid, token_time = err.payload.decode().split(".")
        token_signed = generate_session_token(token_uuid)
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid session")
    return token_signed


def get_user_by_token(token: str) -> dict[str, str]:
    signer = TimestampSigner(secret_key=settings.secret.get_secret_value())
    try:
        token_uuid, token_time = signer.unsign(token).decode().split(".")
    except BadData:
        raise HTTPException(status_code=400, detail="something wrong occurred")
    else:
        for item in db:
            if item.uuid == token_uuid:
                return item.model_dump()
        raise HTTPException(status_code=404, detail="user not found")


@app.post("/login/")
async def login(
        *,
        user: Annotated[User, Body(
            openapi_examples={
                "example": {
                    "value": {
                        "user": "user123",
                        "password": "password123"
                    }
                }
            }

        )
        ],
        response: Response
) -> Any:
    for item in db:
        if item.user == user.user \
                and item.password == user.password:
            if item.uuid is None:
                item.uuid = str(uuid.uuid4())
            token = generate_session_token(item.uuid)
            set_cookie(token, response)
            return {"message": "login successful"}
        return {"username or password is incorrect"}


@app.get("/profile/", response_model=UserOut)
async def get_user_info(
        response: Response,
        session_token: Annotated[str | None, Cookie()] = None
) -> Any:
    if session_token \
            and (new_token := check_session_token(session_token)):
        if new_token != session_token:
            set_cookie(new_token, response)
        return get_user_by_token(new_token)
    else:
        raise HTTPException(status_code=401, detail="Session expired")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
