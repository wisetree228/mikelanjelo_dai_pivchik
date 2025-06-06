"""
Создание таблиц без алембика
"""
from models import engine, Base
import asyncio

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Запускаем функцию
asyncio.run(create_tables())