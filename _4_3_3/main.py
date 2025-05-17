import uvicorn
from fastapi import FastAPI, Depends

from _4_3_3.api.endpoints.auth.router import router as auth_router
from _4_3_3.api.endpoints.protected_resoure.protected_resource import router as protected_resource_router
from _4_3_3.api.endpoints.resources import router as resources_router
from _4_3_3.util import http_bearer, lifespan

app = FastAPI(lifespan=lifespan, dependencies=[Depends(http_bearer)])
app.include_router(auth_router)
app.include_router(protected_resource_router)
app.include_router(resources_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
