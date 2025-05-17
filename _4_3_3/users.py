from enum import StrEnum
from typing import Any

from _4_3_3.api.endpoints.auth.validation import hash_password
from _4_3_3.schemas import UserSchema


class Roles(StrEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


users_db: dict[str, UserSchema] = {
    "admin": UserSchema(
        username="admin",
        password=hash_password("hard"),
        role=Roles.ADMIN
    ),
    "alice": UserSchema(
        username="alice",
        password=hash_password("week"),
        role=Roles.USER
    ),
    "bob": UserSchema(
        username="bob",
        password=hash_password("week_too"),
        role=Roles.USER
    ),
    "guest": UserSchema(
        username="guest",
        password=hash_password("none"),
        role=Roles.GUEST
    )
}
refresh_tokens: dict[str, str] = {}

resources: dict[str, dict[str, Any]] = {
    "alice": {"content": "Секретные данные Алисы", "is_public": False},
    "bob": {"content": "Публичные заметки Боба", "is_public": True},
    "admin": {"content": "Админский ресурс", "is_public": False}
}
