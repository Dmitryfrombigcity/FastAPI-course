# authentication

from datetime import datetime, UTC, timedelta
from typing import Any

import jwt

from _4_2_3.config import auth_settings


def create_access_token(username: str) -> str:
    jwt_payload = {
        "type": "access",
        "sub": username,
    }
    return encode_jwt(jwt_payload, auth_settings.access_token_expire_minutes)


def create_refresh_token(username: str) -> str:
    jwt_payload = {
        "type": "refresh",
        "sub": username,
    }
    return encode_jwt(jwt_payload, auth_settings.refresh_token_expire_minutes)


def encode_jwt(
        payload: dict[str, Any],
        expire_minutes: int,
        private_key: str = auth_settings.private_key_path.read_text(),
        algorithm: str = auth_settings.algorithm,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str,
        public_key: str = auth_settings.public_key_path.read_text(),
        algorithm: str = auth_settings.algorithm,
) -> dict[str, Any]:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
