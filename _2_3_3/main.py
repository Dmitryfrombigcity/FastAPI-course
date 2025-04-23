# main.py

from typing import Annotated

import uvicorn
from fastapi import FastAPI, Body

from _2_3_3.schemas import Feedback

app = FastAPI()

feedbacks: list[dict[str, str]] = []


@app.post("/feedback/")
async def fetch_feedback(
        *,
        is_premium: bool = False,
        item: Annotated[
            Feedback,
            Body(
                openapi_examples={
                    "standard": {
                        "value": {
                            "name": "Артём",
                            "message": "Понравилась структура курса: теория сразу закрепляется практикой",
                            "contact": {
                                "email": "artem@study.ru"
                            }
                        },
                    },
                    "standard_with_phone": {
                        "value": {
                            "name": "Виктория",
                            "message": "Подробные примеры из реальных проектов помогают понять нюансы разработки",
                            "contact": {
                                "email": "vika@protonmail.com",
                                "phone": "79051234567"
                            }
                        },
                    },
                    "bad_message": {
                        "value": {
                            "name": "Виктория",
                            "message": "Этот козявка испортил весь курс, это возмутительно и неприемлемо!",
                            "contact": {
                                "email": "vika@protonmail.com",
                                "phone": "79051234567"
                            }
                        },
                    },
                    "bad_phone_number": {
                        "value": {
                            "name": "Виктория",
                            "message": "Этот *** испортил весь курс, это возмутительно и неприемлемо!",
                            "contact": {
                                "email": "vika@protonmail.com",
                                "phone": "7905123a"
                            }
                        },
                    },
                },
            )
        ]

) -> dict[str, str]:
    feedbacks.append(item.model_dump())
    response = {"message": f"Спасибо, {item.name}! Ваш отзыв сохранён."}
    if is_premium:
        response["message"] = response["message"] + " Ваш отзыв будет рассмотрен в приоритетном порядке."
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
