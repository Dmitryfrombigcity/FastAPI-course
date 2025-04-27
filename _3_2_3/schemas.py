# schemas.py

from pydantic import BaseModel


class UserOut(BaseModel):
    user: str
    password: str


class User(UserOut):
    uuid: str | None = None
