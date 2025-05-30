from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.async_session_generator import get_db
from db.models import *

async def get_or_create_new_user(chat_id: int):
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id==chat_id))
        user = result_db.scalars().first()
        if user:
            return user
        new_user = User(
            id=chat_id
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return User


async def set_name(user_id: int, name: str):
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.name = name
        await db.commit()
