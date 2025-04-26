# main.py

from typing import Any

import uvicorn
from fastapi import FastAPI

from _3_1_2.schemas import goods

app = FastAPI()


@app.get("/product/{product_id}")
async def get_product(product_id: int) -> Any:
    for item in goods:
        if item.product_id == product_id:
            return item.model_dump()
    return "Product not found"


@app.get("/products/search/")
async def get_products(
        keyword: str,
        category: str | None = None,
        limit: int = 10
) -> Any:
    response: list[dict[str, Any]] = []

    for item in goods:
        if not limit:
            break

        if keyword.lower() in item.name.lower():
            if category:
                if category.lower() == item.category.lower():
                    response.append(item.model_dump())
            else:
                response.append(item.model_dump())
            limit -= 1

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
