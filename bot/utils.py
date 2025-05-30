from aiogram import types

async def check_any_content(message: types.Message):
    if message.document or message.audio or message.video or message.photo or message.voice or message.animation or message.video_note or message.sticker:
        return True