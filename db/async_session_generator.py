"""
генератор сессии бд
"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from db.models import engine
from contextlib import asynccontextmanager

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def get_db():
    """
    Генератор асинхронной сессии бд
    :return:
    """
    async with SessionLocal() as session:
        yield session