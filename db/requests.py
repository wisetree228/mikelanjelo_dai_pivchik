"""
Функции для обращения к бд
"""
import random
from sqlalchemy import select, and_, or_, delete, update
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from db.async_session_generator import get_db
from db.models import *

async def get_or_create_new_user(chat_id: int, change_us: bool = False, username: str = None):
    """
    Принимает на вход id телеграм аккаунта и возвращает
    привязанного к нему пользователя (если его нет, создаёт).
    Если указать change_us = True, она обновит этому пользователю юзернейм
    :param chat_id: id аккаунта
    :param change_us: обновить ли юзернейм
    :param username: юзернейм
    :return: User
    """
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
    """
    Записывает пользователю с указанным id указанное имя
    :param user_id:
    :param name:
    :return:
    """
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.name = name
        await db.commit()


async def set_age(user_id: int, age: int):
    """
    Записывает пользователю с указанным id указанный возраст
    :param user_id:
    :param age:
    :return:
    """
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.age = age
        await db.commit()


async def set_gender(user_id: int, gender: str):
    """
    Записывает пользователю с указанным id указанный пол
    :param user_id:
    :param gender:
    :return:
    """
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.gender = gender
        await db.commit()


async def set_description(user_id: int, description: str):
    """
    Записывает пользователю с указанным id указанное описание
    :param user_id:
    :param description:
    :return:
    """
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.about = description
        await db.commit()


async def set_who_search(user_id: int, target: str):
    """
    Записывает пользователю с указанным id параметр того кого он ищет
    :param user_id:
    :param description:
    :return:
    """
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.who_search = target
        await db.commit()


async def add_user_media(user_id: int, media: bytes, type: str):
    """
    Добавляет в базу данных фото или видео пользователя
    :param user_id:
    :param media: байты файла
    :param type: тип (photo или video)
    :return:
    """
    async with get_db() as db:
        new_media = Media(
            user_id=user_id,
            file=media,
            media_type=type
        )
        db.add(new_media)
        await db.commit()


async def delete_media(user_id: int):
    """
    Удаляет все медиафайлы пользователя
    :param user_id:
    :return:
    """
    async with get_db() as db:
        result = await db.execute(select(Media).filter(Media.user_id==user_id))
        media = result.scalars().all()
        for med in media:
            await db.delete(med)
        await db.commit()


async def get_user_media(user_id: int):
    """
    Возвращает список обьектов Media пользователя
    :param user_id:
    :return:
    """
    async with get_db() as db:
        result = await db.execute(select(Media).filter(Media.user_id==user_id))
        return result.scalars().all()


async def get_random_anket_for_match(user_id: int):
    """
    Выбирает случайную анкету, подходящую для мэтча:
    - по полу и возрасту
    - в одном городе ИЛИ (если есть координаты у обоих) на расстоянии <= 5 км
    """
    async with get_db() as db:
        user = await get_or_create_new_user(chat_id=user_id)
        if not user:
            return None

        # Базовые условия (пол, возраст, кто ищет)
        base_conditions = [
            User.age <= user.age + 2,
            User.age >= user.age - 2,
            or_(
                User.who_search == user.gender,
                User.who_search == 'A'
            ),
            User.id != user_id
        ]

        # Условие по полу (если нужно)
        if user.who_search in ['M', 'W']:
            base_conditions.insert(0, User.gender == user.who_search)

        # Условия близости: город ИЛИ расстояние
        proximity_condition = User.city == user.city  # Всегда проверяем город

        # Если у пользователя есть координаты - добавляем вариант с расстоянием
        if user.lat is not None and user.lon is not None:
            # Создаем подзапрос для проверки расстояния
            distance_condition = and_(
                User.lat.is_not(None),
                User.lon.is_not(None),
                User.haversine_expression(User.lat, User.lon, user.lat, user.lon) <= 5
            )
            proximity_condition = or_(
                proximity_condition,
                distance_condition
            )

        # Объединяем все условия
        query = select(User).where(
            and_(
                *base_conditions,
                proximity_condition
            )
        ).order_by(func.random())

        result = await db.execute(query)
        users = result.scalars().all()

        return random.choice(users) if users else None


async def create_like(author_id: int, getter_id: int):
    """
    Записывает в бд лайк от одного пользователя другому
    :param author_id:
    :param getter_id:
    :return:
    """
    async with get_db() as db:
        like = Like(
            getter_id=getter_id,
            author_id=author_id
        )
        db.add(like)
        await db.commit()


async def get_likes_count(user_id: int):
    """
    Возвращает пользователю количество лайков которые поставили на его анкету
    :param user_id:
    :return:
    """
    async with get_db() as db:
        count = await db.execute(select(func.count(Like.id)).where(Like.getter_id == user_id))
        return count.scalar_one()


async def get_first_got_like_anket(user_id: int):
    """
    Возвращает пользователю первого из юзеров которые его лайкнули
    :param user_id:
    :return:
    """
    async with get_db() as db:
        result = await db.execute(select(Like).where(Like.getter_id == user_id).options(
            joinedload(Like.author)
        ))
        like = result.scalars().first()
        return like.author


async def delete_likes_between_users(first_user_id: int, second_user_id: int):
    """
    Удаляет лайки между двумя пользователями
    :param first_user_id:
    :param second_user_id:
    :return:
    """
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


async def set_coordinates(user_id: int, lat: float = None, lon: float = None):
    """
    Меняет координаты пользователя
    :param user_id:
    :param lat:
    :param lon:
    :return:
    """
    async with get_db() as db:
        stmt = update(User).where(User.id == user_id).values(lon = lon, lat = lat)
        await db.execute(stmt)
        await db.commit()


async def set_city(user_id: int, city: str):
    """
    Записывает пользователю с указанным id указанное имя
    :param user_id:
    :param name:
    :return:
    """
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id == user_id))
        user = result_db.scalars().first()
        user.city = city
        await db.commit()


async def exists_like_between_two_users(author_id: int, getter_id: int):
    """
    Проверяет существование лайков между двумя пользователями (во избежание дублирования)
    :param author_id:
    :param getter_id:
    :return:
    """
    async with get_db() as db:
        result = await db.execute(select(Like).filter(
            and_(
                Like.author_id == author_id,
                Like.getter_id == getter_id
            )
        ))
        like = result.scalars().first()
        if like:
            return True
        return False