# main.py

from datetime import datetime
from typing import Annotated, Any

import uvicorn
from fastapi import FastAPI, Header, Response
from fastapi.encoders import jsonable_encoder

from _3_3_3.schemas import CommonHeaders

app = FastAPI()


@app.get("/headers/")
async def get_headers(headers: Annotated[CommonHeaders, Header()]) -> Any:
    return {"User-Agent": headers.user_agent, "Accept-Language": headers.accept_language}


@app.get("/info/")
async def get_info(headers: Annotated[CommonHeaders, Header()], response: Response) -> Any:
    response.headers["X-Server-Time"] = jsonable_encoder(datetime.now())
    return {"message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
            "headers": {
                "User-Agent": headers.user_agent, "Accept-Language": headers.accept_language}
            }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
