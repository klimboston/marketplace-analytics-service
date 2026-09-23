from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.marketplace_analytics_service.core.database import engine, sessionmaker


async def get_session():
    async with sessionmaker() as session:
        yield session
        
SessionDep = Annotated[AsyncSession, Depends(get_session)]