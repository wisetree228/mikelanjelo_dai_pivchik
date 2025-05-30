from db.requests import *
from aiogram.fsm.context import FSMContext
from aiogram import types
from bot.states import Form
from bot.keyboards import *
from bot.utils import *

async def start_controller(message: types.Message, state: FSMContext):
    user = await get_or_create_new_user(chat_id=message.chat.id)
    if not(user.name):
        await message.answer(f"Привет! Для твоего аккаунта не найдено уже существующих данных, видимо ты новичок. Чтобы пользоваться нашим ресурсом, тебе необходимо заполнить анкету. Введи своё имя:")
        await state.set_state(Form.name)
    else:
        await message.answer('Привет! Это бот для знакомств "Микелянджело дай пивчик", главный конкурент "Леонардо дай винчика". Выбери опцию:', reply_markup=main_menu_keyboard)


async def edit_profile_controller(message: types.Message, state: FSMContext):
    await message.answer('Хорошо, давай заполним твою анкету заново! Введи своё имя:')
    await state.set_state(Form.name)


async def set_name_controller(message: types.Message, state: FSMContext):
    if await check_any_content(message):
        await message.answer("Отправьте только текст!")
        await state.set_state(Form.name)
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
    if await check_any_content(message):
        await message.answer("Отправьте только текст!")
        await state.set_state(Form.age)
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
    if await check_any_content(message):
        await message.answer("Отправьте только текст!")
        await state.set_state(Form.gender)
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
    if await check_any_content(message):
        await message.answer("Отправьте только текст!")
        await state.set_state(Form.description)
    if len(message.text)>1000:
        await message.answer(
            "Слишком длинное описание! Введите описание не длиннее 1000 символов:")
        await state.set_state(Form.description)
    else:
        await set_description(user_id=message.chat.id, description=message.text)
        await message.answer(
            "Ваше описание записано в базу данных! Теперь отправьте до 3 фото и/или видео"
        )
        await state.set_state(Form.media)


async def edit_media_controller(message: types.Message, state: FSMContext):
    if not message.photo and not message.video:
        await message.answer('Отправьте картинки и/или видео, другой формат информации не принимается!')
        await state.set_state(Form.media)
    else:
        total_files = 0
        if message.photo:
            total_files += 1
        if message.video:
            total_files += 1

        if total_files > 3:
            await message.answer('Максимум 3 файла!')
            await state.set_state(Form.media)
        else:
            bot = message.bot
            await delete_media(user_id=message.chat.id)

            if message.photo:
                largest_photo = message.photo[-1]
                file_id = largest_photo.file_id
                file = await bot.get_file(file_id)
                photo = await bot.download_file(file.file_path)
                photo_bytes = photo.read()
                await add_user_media(user_id=message.chat.id, media=photo_bytes, type='photo')

            if message.video:
                file_id = message.video.file_id
                file = await bot.get_file(file_id)
                video = await bot.download_file(file.file_path)
                video_bytes = video.read()
                await add_user_media(user_id=message.chat.id, media=video_bytes, type='video')