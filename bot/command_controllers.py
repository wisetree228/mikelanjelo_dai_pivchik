from db.requests import get_or_create_new_user, set_name
from aiogram.fsm.context import FSMContext
from aiogram import types
from bot.states import Form

async def start_controller(message: types.Message, state: FSMContext):
    user = await get_or_create_new_user(chat_id=message.chat.id)
    if not(user.name):
        await message.answer(f"Привет! Для твоего аккаунта не найдено данных, видимо ты новичок. Чтобы пользоваться нашим ресурсом, тебе необходимо заполнить анкету. Введи своё имя:")
        await state.set_state(Form.name)


async def set_name_controller(message: types.Message, state: FSMContext):
    user = await get_or_create_new_user(chat_id=message.chat.id)
    await set_name(user.id, message.text)
    await message.answer("Твоё имя изменено!")