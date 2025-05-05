# users

from _4_2_1.schemas import UserSchema
from _4_2_1.utils import hash_password

first = UserSchema(
    username="first",
    password=hash_password("hard"),
)
second = UserSchema(
    username="second",
    password=hash_password("low"),
)

users_db: dict[str, UserSchema] = {
    first.username: first,
    second.username: second,
}
