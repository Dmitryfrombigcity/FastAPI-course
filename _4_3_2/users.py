# users
from enum import StrEnum

from _4_3_2.schemas import UserSchema
from _4_3_2.validation import hash_password


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
    "user": UserSchema(
        username="user",
        password=hash_password("week"),
        role=Roles.USER
    ),
    "guest": UserSchema(
        username="guest",
        password=hash_password("none"),
        role=Roles.GUEST
    )
}
refresh_tokens: dict[str, str] = {}
