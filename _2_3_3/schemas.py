# schemas.py

import re
from typing import Annotated

from pydantic import BaseModel, AfterValidator, EmailStr
from pydantic.fields import Field


def check_words(message: str) -> str:
    bad_words = ("редиск", "бяк", "козявк")
    for word in bad_words:
        if re.search(rf"\b{word}\S*\b", message, re.IGNORECASE):
            raise ValueError("Использование недопустимых слов")
    return message


def check_phone_length(phone: int) -> int:
    if 7 <= len(str(phone)) <= 15:
        return phone
    raise ValueError("Использование недопустимого номера телефона")


class Contact(BaseModel):
    email: EmailStr
    phone: Annotated[int | None, AfterValidator(check_phone_length)] = None


class Feedback(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    message: Annotated[str, Field(min_length=10, max_length=500), AfterValidator(check_words)]
    contact: Contact
