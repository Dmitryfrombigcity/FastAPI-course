# main.py

from typing import Annotated

import uvicorn
from fastapi import FastAPI, Body

from _2_3_2.schemas import Feedback

app = FastAPI()

feedbacks: list[dict[str, str]] = []


@app.post("/feedback/")
async def fetch_feedback(
        item: Annotated[
            Feedback,
            Body(
                openapi_examples={
                    "correct":
                        {
                            "value":
                                {
                                    "name": "Анна",
                                    "message": "Этот курс заставляет меня напрячься, но я все равно его пройду!"
                                },
                        },
                    "incorrect":
                        {
                            "value":
                                {
                                    "name": "А",
                                    "message": "тут сплошные редиски кругом, житья совсем не дают"
                                },
                        },
                },
            )
        ]

) -> dict[str, str]:
    feedbacks.append(item.model_dump())
    return {"message": f"Спасибо, {item.name}! Ваш отзыв сохранён."}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
