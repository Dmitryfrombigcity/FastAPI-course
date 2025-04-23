import uvicorn
from fastapi import FastAPI

from _2_3_1.schemas import Feedback

app = FastAPI()

archive: list[dict[str, str]] = []


@app.post("/feedback/")
async def fetch_and_reply(item: Feedback) -> dict[str, str]:
    archive.append(item.model_dump())
    print(archive)
    return {"message": f"Feedback received. Thank you, {item.name}."}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
