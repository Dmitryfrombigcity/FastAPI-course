# main.py

import uuid
from typing import Annotated, Any

import uvicorn
from fastapi import FastAPI, Response, HTTPException, Body, Cookie
from itsdangerous import URLSafeTimedSerializer, BadData

from _3_2_2.config import settings
from _3_2_2.schemas import User

app = FastAPI()

db = {
    "user123": {
        "password": "password123"
    },
    "user124": {
        "password": "password124"
    }
}

session: dict[str, str] = {}


def generate_session_token() -> str:
    token_uuid = str(uuid.uuid4()).replace("-", "")
    token_serializer = URLSafeTimedSerializer(secret_key=settings.secret.get_secret_value())
    token_signed = token_serializer.dumps(token_uuid)
    return token_signed


def check_session_token(token: str) -> bool:
    is_valid = True
    token_serializer = URLSafeTimedSerializer(secret_key=settings.secret.get_secret_value())
    try:
        token_serializer.loads(token, max_age=settings.max_age)
    except BadData:
        is_valid = False
    return is_valid


@app.post("/login/")
def login(
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
    if db.get(user.user) \
            and db.get(user.user).get("password") == user.password:
        value = generate_session_token()
        response.set_cookie(
            key="session_token",
            value=value,
            secure=True,
            httponly=True,
            # max_age=settings.max_age
        )
        session[value] = user.user
        return {"message": "login successful"}
    else:
        return {"username or password is incorrect"}


@app.get("/profile/")
def get_user_info(session_token: Annotated[str | None, Cookie()] = None) -> Any:
    if (user := session.get(session_token)) \
            and check_session_token(session_token):
        return {"user": user} | db.get(user)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
