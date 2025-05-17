# schemas

from pathlib import Path

from pydantic import BaseModel

BASE_DIR = Path(".")


class User(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    username: str
    password: bytes
    role: str


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 7 * 24 * 60
