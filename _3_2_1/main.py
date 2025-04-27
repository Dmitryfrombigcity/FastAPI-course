import uuid
from typing import Annotated, Any

import uvicorn
from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Cookie

from _3_2_1.schemas import User

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
    token = str(uuid.uuid4()).replace("-", "")
    return token


@app.post("/login/")
def login(user: User, response: Response) -> Any:
    if db.get(user.user) \
            and db.get(user.user).get("password") == user.password:
        value = generate_session_token()
        response.set_cookie(
            key="session_token",
            value=value,
            secure=True,
            httponly=True
        )
        session[value] = user.user
        return {"message": "login successful"}
    else:
        return {"username or password is incorrect"}


@app.get("/user")
def get_user_info(session_token: Annotated[str | None, Cookie()] = None) -> Any:
    if user := session.get(session_token):
        return {"user": user} | db.get(user)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
