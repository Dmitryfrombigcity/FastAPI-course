# users

from _4_2_3.schemas import UserSchema

users_db: dict[str, UserSchema] = {}
refresh_tokens: dict[str, str] = {}
