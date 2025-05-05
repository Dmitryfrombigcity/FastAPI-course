# main.py

from typing import Any, Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from _4_2_1.schemas import User
from _4_2_1.users import users_db
from _4_2_1.utils import create_access_token, decode_jwt, validate_password

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def is_valid_token(token: Annotated[str, Depends(oauth2_scheme)]) -> None:
    try:
        decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error",
            headers={"WWW-Authenticate": "Bearer"}
        )


def authenticate_user(user: User) -> None:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password")
    if not (user_schema := users_db.get(user.username)):
        raise unauthed_exc
    if not validate_password(
            password=user.password,
            hashed_password=user_schema.password
    ):
        raise unauthed_exc


@app.post("/login/", dependencies=[Depends(authenticate_user)])
async def sign_in(user: User) -> Any:
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected_resource/", dependencies=[Depends(is_valid_token)])
async def get_resource() -> Any:
    return {"message": "access granted"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
