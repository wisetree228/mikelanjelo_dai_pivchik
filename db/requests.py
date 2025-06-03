from sqlalchemy import select, and_, or_, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from db.async_session_generator import get_db
from db.models import *

async def get_or_create_new_user(chat_id: int, change_us: bool = False, username: str = None):
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id==chat_id))
        user = result_db.scalars().first()
        if user:
            if change_us:
                user.username = username
                await db.commit()
            return user
        if username is None:
            new_user = User(
                id=chat_id
            )
        else:
            new_user = User(
                id=chat_id,
                username=username
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


async def get_random_anket_for_match(user_id: int):
    async with get_db() as db:
        user = await get_or_create_new_user(chat_id=user_id)
        if user.who_search == 'M':
            result = await db.execute(select(User).filter(
                and_(
                    User.gender=='M',
                    User.age<=user.age+2,
                    User.age>=user.age-2,
                    or_(
                        User.who_search == user.gender,
                        User.who_search == 'A'
                    ),
                    User.id != user_id
                )
            ).order_by(func.random()).limit(1))
            another_user = result.scalars().first()
        elif user.who_search == 'W':
            result = await db.execute(select(User).filter(
                and_(
                    User.gender == 'W',
                    User.age <= user.age + 2,
                    User.age >= user.age - 2,
                    or_(
                        User.who_search == user.gender,
                        User.who_search == 'A'
                    ),
                    User.id != user_id
                )
            ).order_by(func.random()).limit(1))
            another_user = result.scalars().first()
        else:
            result = await db.execute(select(User).filter(
                and_(
                    User.age <= user.age + 2,
                    User.age >= user.age - 2,
                    or_(
                        User.who_search == user.gender,
                        User.who_search == 'A'
                    ),
                    User.id != user_id
                )
            ).order_by(func.random()).limit(1))
            another_user = result.scalars().first()
        return another_user


async def create_like(author_id: int, getter_id: int):
    async with get_db() as db:
        like = Like(
            getter_id=getter_id,
            author_id=author_id
        )
        db.add(like)
        await db.commit()


async def get_likes_count(user_id: int):
    async with get_db() as db:
        count = await db.execute(select(func.count(Like.id)).where(Like.getter_id == user_id))
        return count.scalar_one()


async def get_first_got_like_anket(user_id: int):
    async with get_db() as db:
        result = await db.execute(select(Like).where(Like.getter_id == user_id).options(
            joinedload(Like.author)
        ))
        like = result.scalars().first()
        return like.author


async def delete_likes_between_users(first_user_id: int, second_user_id: int):
    async with get_db() as db:
        await db.execute(delete(Like).where(
            or_(
                and_(
                    Like.author_id == first_user_id,
                    Like.getter_id == second_user_id
                ),
                and_(
                    Like.author_id == second_user_id,
                    Like.getter_id == first_user_id
                )
            )
        ))
        await db.commit()