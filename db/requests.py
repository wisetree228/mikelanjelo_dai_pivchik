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
        return new_user


async def set_name(user_id: int, name: str):
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.name = name
        await db.commit()


async def set_age(user_id: int, age: int):
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.age = age
        await db.commit()


async def set_gender(user_id: int, gender: str):
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.gender = gender
        await db.commit()


async def set_description(user_id: int, description: str):
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.about = description
        await db.commit()


async def set_who_search(user_id: int, target: str):
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.who_search = target
        await db.commit()


async def add_user_media(user_id: int, media: bytes, type: str):
    async with get_db() as db:
        new_media = Media(
            user_id=user_id,
            file=media,
            media_type=type
        )
        db.add(new_media)
        await db.commit()


async def delete_media(user_id: int):
    async with get_db() as db:
        result = await db.execute(select(Media).filter(Media.user_id==user_id))
        media = result.scalars().all()
        for med in media:
            await db.delete(med)
        await db.commit()


async def get_user_media(user_id: int):
    async with get_db() as db:
        result = await db.execute(select(Media).filter(Media.user_id==user_id))
        return result.scalars().all()
