from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.marketplace_analytics_service.core.database import init_db
from src.marketplace_analytics_service.routers import marketplaces


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=marketplaces.router)


@app.get("/healthcheck")
async def lifecheck():
    return {"status": "ok"}
