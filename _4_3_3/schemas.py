from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    username: str
    password: bytes
    role: str
