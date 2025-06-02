from aiogram import types, Bot
from typing import List
from aiogram.exceptions import TelegramAPIError
from db.models import *
import tempfile

async def check_any_content(message: types.Message):
    if message.document or message.audio or message.video or message.photo or message.voice or message.animation or message.video_note or message.sticker:
        return True
    return False


async def send_media_group_with_caption(media_items: List[Media], caption: str, bot: Bot, chat_id: int):
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


async def get_caption_for_user(user: User):
    caption = (
        f"Имя: {user.name}\n"
        f"Пол (M - man, W - woman): {user.gender}\n"
        f"Возраст: {user.age}\n"
        f"Описание:\n{user.about}\n\n\n"
    )
    return caption