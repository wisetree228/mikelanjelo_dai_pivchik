"""
Вспомогательные функции для бота
"""
from aiogram import types, Bot
from typing import List
from aiogram.exceptions import TelegramAPIError
from db.models import *
import tempfile

async def check_any_content(message: types.Message):
    """
    Проверяет, есть ли в сообщении что-то кроме текста
    :param message:
    :return:
    """
    if message.document or message.audio or message.video or message.photo or message.voice or message.animation or message.video_note or message.sticker:
        return True
    return False


async def send_media_group_with_caption(media_items: List[Media], caption: str, bot: Bot, chat_id: int):
    """
    Отправляет группу медиафайлов (обьектов Media) в чат
    :param media_items: список Media
    :param caption: подпись в сообщении
    :param bot: бот, который отправляет
    :param chat_id: id чата в который отправляем
    :return:
    """
    media_group = []
    temp_files = []
    for i, media_item in enumerate(media_items):
        try:
            # Создаем временный файл
            suffix = '.jpg' if media_item.media_type == 'photo' else '.mp4'
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(media_item.file)
                temp_path = temp_file.name
                temp_files.append(temp_path)

            # Создаем медиа объект
            if media_item.media_type == 'photo':
                media = types.InputMediaPhoto(
                    media=types.FSInputFile(temp_path),
                    caption=caption if i == 0 else None
                )
            elif media_item.media_type == 'video':
                media = types.InputMediaVideo(
                    media=types.FSInputFile(temp_path),
                    caption=caption if i == 0 else None
                )
            else:
                continue

            media_group.append(media)

        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            # Удаляем временные файлы при ошибке
            for path in temp_files:
                try:
                    os.unlink(path)
                except:
                    pass
            return
    try:
        await bot.send_media_group(chat_id=chat_id, media=media_group)
    finally:
        # Удаляем временные файлы после отправки
        for path in temp_files:
            try:
                os.unlink(path)
            except:
                pass


async def get_caption_for_user(user: User, user_who_search: User):
    """
    Возвращает описание анкеты для пользователя
    :param user: обьект User
    :param user_who_search: обьект юзера который получает анкету (для проверки расстояния)
    :return:
    """
    if not( user.lat and user.lon and user_who_search.lat and user_who_search.lon ):
        caption = (
            f"Имя: {user.name}\n"
            f"Пол (M - man, W - woman): {user.gender}\n"
            f"Возраст: {user.age}\n"
            f"Город: {user.city}\n"
            f"Описание:\n{user.about}\n\n\n"
        )
    else:
        caption = (
            f"Имя: {user.name}\n"
            f"Пол (M - man, W - woman): {user.gender}\n"
            f"Возраст: {user.age}\n"
            f"Город: {user.city}\n"
            f"Расстояние: {round(user.haversine(user.lat, user.lon, user_who_search.lat, user_who_search.lon), 1)} км от вас\n"
            f"Описание:\n{user.about}\n\n\n"
        )
    return caption