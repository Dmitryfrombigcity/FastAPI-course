# schemas.py

import re
from typing import Annotated

from pydantic import BaseModel, AfterValidator
from pydantic.fields import Field


def check_words(message: str) -> str:
    bad_words = ("редиск", "бяк", "козявк")
    for word in bad_words:
        if re.search(rf"\b{word}\S*\b", message, re.IGNORECASE):
            raise ValueError("Использование недопустимых слов")
    return message


class Feedback(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    message: Annotated[str, Field(min_length=10, max_length=500), AfterValidator(check_words)]
