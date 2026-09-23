import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from src.marketplace_analytics_service.core.config import settings
from src.marketplace_analytics_service.core.models import MarketPlace

engine = create_async_engine(settings.database_url, echo=True)

sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        
redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)
        