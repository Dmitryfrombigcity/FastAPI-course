# schemas.py

from typing import Annotated

from pydantic import BaseModel, AfterValidator, Field

MINIMUM_APP_VERSION = "0.0.2"


def check_version(version: str) -> str:
    min_version = tuple(map(int, MINIMUM_APP_VERSION.split(".")))
    current_version = tuple(map(int, version.split(".")))
    if current_version < min_version:
        raise ValueError("Требуется обновить приложение")
    return version


class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str
    x_current_version: Annotated[str, Field(pattern=r"^\d+\.\d+\.\d+$"), AfterValidator(check_version)]
