from db.requests import *
from aiogram.fsm.context import FSMContext
from aiogram import types
from bot.states import Form
from bot.keyboards import choose_gender_keyboard

async def start_controller(message: types.Message, state: FSMContext):
    user = await get_or_create_new_user(chat_id=message.chat.id)
    if not(user.name):
        await message.answer(f"Привет! Для твоего аккаунта не найдено данных, видимо ты новичок. Чтобы пользоваться нашим ресурсом, тебе необходимо заполнить анкету. Введи своё имя:")
        await state.set_state(Form.name)


async def set_name_controller(message: types.Message, state: FSMContext):
    user = await get_or_create_new_user(chat_id=message.chat.id)
    if len(message.text)>50:
        await message.answer(
            f"Имя слишком длинное, введи имя не длиннее 50 символов:")
        await state.set_state(Form.name)
    else:
        await set_name(user_id=user.id, name=message.text)
        await message.answer("Твоё имя записано в базу данных! Теперь введи свой возраст:")
        await state.set_state(Form.age)


async def set_age_controller(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(
            f"Некорректный формат, введи только цифры")
        await state.set_state(Form.age)
    elif int(message.text)>130 or int(message.text)<=0:
        await message.answer(
            f"Некорректный формат, введи возраст от 1 до 130:")
        await state.set_state(Form.age)
    else:
        await set_age(user_id=message.chat.id, age=int(message.text))
        await message.answer("Твой возраст записан в базу данных! Теперь выбери пол:", reply_markup=choose_gender_keyboard)
        await state.set_state(Form.gender)


async def set_gender_controller(message: types.Message, state: FSMContext):
    if message.text == "Мужчина":
        await set_gender(user_id=message.chat.id, gender='M')
        await message.answer("Ваш пол записан в базу данных! Теперь введите краткое описание своей анкеты, расскажите немного о себе(не больше 1000 символов):")
        await state.set_state(Form.description)
    elif message.text == "Женщина":
        await set_gender(user_id=message.chat.id, gender='W')
        await message.answer(
            "Ваш пол записан в базу данных! Теперь введите краткое описание своей анкеты, расскажите немного о себе(не больше 1000 символов):")
        await state.set_state(Form.description)
    else:
        await message.answer("Некорректный формат пола! Воспользуйтесь клавиатурой для выбора пола:",
                             reply_markup=choose_gender_keyboard)
        await state.set_state(Form.gender)


async def set_description_controller(message: types.Message, state: FSMContext):
    if len(message.text)>1000:
        await message.answer(
            "Слишком длинное описание! Введите описание не длиннее 1000 символов:")
        await state.set_state(Form.description)
    else:
        await set_description(user_id=message.chat.id, description=message.text)
        await message.answer(
            "Ваше описание записано в базу данных!"
        )
        #await state.set_state(...)