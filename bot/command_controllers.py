"""
обработчики команд (основная логика)
"""
from aiogram.exceptions import TelegramAPIError
from aiogram.enums import ParseMode
import tempfile
import os
from db.requests import *
from aiogram.fsm.context import FSMContext
from aiogram import types
from bot.states import Form
from bot.keyboards import *
from bot.utils import *
from re import sub

async def start_controller(message: types.Message, state: FSMContext):
    """
    Обработка команды /start. Предлагает пользователю заполнить анкету (если о нём нет данных) или выбрать опцию из главного меню
    :param message:
    :param state:
    :return:
    """
    user = await get_or_create_new_user(chat_id=message.chat.id, username=message.from_user.username, change_us=True)
    if (user.name is None) or (user.about is None) or (user.gender is None) or (user.age is None) or not(await get_user_media(user_id=message.chat.id)) or (user.who_search is None):
        await message.answer(f"Привет! Для твоего аккаунта не найдено уже существующих данных или данные не полные, видимо ты новичок. Чтобы пользоваться нашим ресурсом, тебе необходимо заполнить анкету. Введи своё имя:")
        await state.set_state(Form.name)
    else:
        await message.answer('Привет! Это бот для знакомств "Микелянджело дай пивчик", главный конкурент "Леонардо дай винчика". Выбери опцию:', reply_markup=await get_main_menu_keyboard(await get_likes_count(message.chat.id)))
        await state.set_state(Form.main_menu)


async def edit_profile_controller(message: types.Message, state: FSMContext):
    """
    Обработка команды /edit. Заново заполняет анкету пользователя
    :param message:
    :param state:
    :return:
    """
    await message.answer('Хорошо, давай заполним твою анкету заново! Введи своё имя:')
    await get_or_create_new_user(chat_id=message.chat.id, change_us=True, username=message.from_user.username)
    await state.set_state(Form.name)


async def set_name_controller(message: types.Message, state: FSMContext):
    """
    Меняет имя пользователя
    :param message:
    :param state:
    :return:
    """
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
        await message.answer("Отлично! Теперь введи свой возраст:")
        await state.set_state(Form.age)


async def set_age_controller(message: types.Message, state: FSMContext):
    """
    Меняет возраст пользователя
    :param message:
    :param state:
    :return:
    """
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
    """
    Меняет пол пользователя
    :param message:
    :param state:
    :return:
    """
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
    """
    Меняет описание пользователя
    :param message:
    :param state:
    :return:
    """
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
            "Теперь укажи, какие анкеты тебе показывать:",
            reply_markup=choose_who_you_search
        )
        await state.set_state(Form.who_search)


async def who_search_controller(message: types.Message, state: FSMContext):
    """
    Меняет предпочтения пользователя (кого он ищет)
    :param message:
    :param state:
    :return:
    """
    if message.text == "Мужчин":
        await set_who_search(user_id=message.chat.id, target="M")
        await message.answer("Хорошо! Теперь отправьте до 3 фото и/или видео для своей анкеты (все ваши предыдущие фото и видео будут удалены и перезаписаны)")
        await state.set_state(Form.media)
    elif message.text == "Женщин":
        await set_who_search(user_id=message.chat.id, target="W")
        await message.answer(
            "Хорошо! Теперь отправьте до 3 фото и/или видео для своей анкеты (все ваши предыдущие фото и видео будут удалены и перезаписаны)")
        await state.set_state(Form.media)
    elif message.text == "Кого угодно":
        await set_who_search(user_id=message.chat.id, target="A")
        await message.answer(
            "Хорошо! Теперь отправьте до 3 фото и/или видео для своей анкеты (все ваши предыдущие фото и видео будут удалены и перезаписаны)")
        await state.set_state(Form.media)
    else:
        await message.answer("Используйте клавиатуру для выбора искомых анкет!", reply_markup=choose_who_you_search)


async def edit_media_controller(message: types.Message, state: FSMContext):
    """
    Меняет медиафайлы (фото и видео) пользователя
    :param message:
    :param state:
    :return:
    """
    if not message.photo and not message.video:
        await message.answer('Отправьте картинки и/или видео, другой формат информации не принимается!')
        await state.set_state(Form.media)
        return
    else:
        total_files = 0
        if message.photo:
            total_files += 1
        if message.video:
            total_files += 1

        if total_files > 3:
            await message.answer('Максимум 3 файла!')
            await state.set_state(Form.media)
            return
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
        await message.answer('Ваши медиа добавлены в базу данных! Теперь по желанию вы можете указать координаты своего местоположения (если не хотите или хотите удалить уже указанные координаты, нажмите "Отказаться"). Пришлите их в виде двух вещественных чисел через пробел, дробная часть должна быть отделена точкой, никаких лишних символов быть не должно. Координаты можно скопировать с любых онлайн-карт',
                             reply_markup=change_coordinates_keyboard)
        await state.set_state(Form.coordinates)


async def change_location_controller(message: types.Message, state: FSMContext):
    if message.text == "Отказаться":
        await set_coordinates(message.chat.id, None, None)
        await message.answer('Хорошо, если вы не указываете координаты то должны указать свой город. Введите название города в котором живёте без сокращений и орфографических ошибок:')
        await state.set_state(Form.city)
    else:
        coords = message.text.split()
        try:
            lat = float(coords[0])
            lon = float(coords[1])
        except:
            await message.answer('Некорректный формат координат! Введите их корректно или нажмите "Отказаться":', reply_markup=change_coordinates_keyboard)
            await state.set_state(Form.coordinates)
            return
        await set_coordinates(message.chat.id, lat, lon)
        await message.answer(
            'Хорошо, теперь укажите свой город. Введите название города в котором живёте без сокращений и орфографических ошибок:')
        await state.set_state(Form.city)


async def edit_city_controller(message: types.Message, state: FSMContext):
    city = sub(r'[^a-zа-яё]', '', message.text.lower())
    if len(city) < 2:
        await message.answer("Слишком короткое название города. Попробуйте ещё раз.")
        return
    if len(city) > 50:
        await message.answer("Слишком длинное название города. Попробуйте ещё раз.")
        return
    await set_city(message.chat.id, city)
    await message.answer("Хорошо, ваша анкета заполнена! Теперь выберите опцию:",
                         reply_markup=await get_main_menu_keyboard(await get_likes_count(message.chat.id)))
    await state.set_state(Form.main_menu)


async def main_menu_controller(message: types.Message, state: FSMContext):
    """
    Обрабатывает команды главного меню
    :param message:
    :param state:
    :return:
    """
    if message.text == "Смотреть мою анкету":
        try:
            await message.answer("Ищем информацию о тебе...")
            user = await get_or_create_new_user(chat_id=message.chat.id, change_us=True, username=message.from_user.username)
            if not user:
                await message.answer("Не удалось найти ваши данные")
                return

            media_items = await get_user_media(message.chat.id)
            if not media_items:
                await message.answer("В вашей анкете нет медиафайлов")
                return


            caption = (
                f"Ваше имя: {user.name}\n"
                f"Ваш пол (M - man, W - woman): {user.gender}\n"
                f"Возраст: {user.age}\n"
                f"Чьи анкеты вы ищете(W-женские, M-мужские, A-все): {user.who_search}\n"
                f"Описание анкеты:\n{user.about}\n\n\n"
                f"Чтобы редактировать свою анкету, нажми /edit\n\n"
                "Важное предупреждение: если в настройках приватности у вас выключена галочка 'предпросмотр ссылок'"
                " и при этом у вас в телеграм нет юзернейма, то пользователь который получит от вас лайк и поставит вам взаимный лайк не сможет получить работающую ссылку на ваш профиль!"
            )
            await send_media_group_with_caption(media_items=media_items, caption=caption, bot=message.bot, chat_id=message.chat.id)
            await message.answer('Если не собираетесь редактировать анкету, выберите одну из предоставленных опций:', reply_markup=await get_main_menu_keyboard(await get_likes_count(message.chat.id)))
            await state.set_state(Form.main_menu)

        except Exception as e:
            await message.answer(f"Произошла непредвиденная ошибка: {e}")

    elif message.text == "Листать анкеты":
        await message.answer("Ищем вам анкету...")
        await get_or_create_new_user(chat_id=message.chat.id, change_us=True, username=message.from_user.username)
        anket = await get_random_anket_for_match(user_id=message.chat.id)
        if not anket:
            await message.answer("Подходящих вам по полу и возрасту анкет пока не зарегистрировано в нашем боте!", reply_markup=await get_main_menu_keyboard(await get_likes_count(message.chat.id)))
            await state.set_state(Form.main_menu)
            return
        media = await get_user_media(anket.id)
        if len(media) == 0:
            await message.answer(await get_caption_for_user(anket)+'\n\nNo photo/video', reply_markup=like_keyboard)
            await state.update_data(object_id=anket.id)
            await state.set_state(Form.like)
            return
        user = await get_or_create_new_user(message.chat.id)
        await send_media_group_with_caption(media_items=media, caption=await get_caption_for_user(anket, user), bot=message.bot, chat_id=message.chat.id)
        await state.update_data(object_id=anket.id)
        await message.answer("Выберите опцию:", reply_markup=like_keyboard)
        await state.set_state(Form.like)

    elif message.text[:15] == "Входящие лайки:":
        await get_or_create_new_user(chat_id=message.chat.id, change_us=True, username=message.from_user.username)
        if await get_likes_count(message.chat.id) == 0:
            await message.answer("Нет входящих лайков!", reply_markup=await get_main_menu_keyboard(await get_likes_count(message.chat.id)))
            await state.set_state(Form.main_menu)
        else:
            anket = await get_first_got_like_anket(user_id=message.chat.id)
            media = await get_user_media(anket.id)
            if len(media) == 0:
                await message.answer(await get_caption_for_user(anket) + '\n\nNo photo/video',
                                     reply_markup=like_keyboard)
                await state.update_data(object_id=anket.id)
                await state.set_state(Form.match)
                return
            await send_media_group_with_caption(media_items=await get_user_media(anket.id), caption="Входящий лайк:\n\n"+await get_caption_for_user(anket), bot=message.bot, chat_id=message.chat.id)
            await message.answer("Выберите опцию:", reply_markup=like_keyboard)
            await state.update_data(object_id=anket.id)
            await state.set_state(Form.match)
    else:
        await message.answer("Введите одну из предоставленных на клавиатуре команд")
        await state.set_state(Form.main_menu)


async def like_controller(message: types.Message, state: FSMContext):
    """
    Обрабатывает лайк или дизлайк на просмотренную анкету
    :param message:
    :param state:
    :return:
    """
    data = await state.get_data()
    anket_id = data.get('object_id')
    if message.text == "Лайк":
        if not(await exists_like_between_two_users(author_id=message.chat.id, getter_id=anket_id)):
            await create_like(author_id=message.chat.id, getter_id=anket_id)
        data.pop('object_id')
        await state.update_data(**data)
        await message.answer('Ваш лайк записан. Выберите опцию:', reply_markup=await get_main_menu_keyboard(await get_likes_count(message.chat.id)))
        await state.set_state(Form.main_menu)
    elif message.text == "Дизлайк":
        data.pop('object_id')
        await state.update_data(**data)
        await message.answer('Окей, выберите опцию:', reply_markup=await get_main_menu_keyboard(await get_likes_count(message.chat.id)))
        await state.set_state(Form.main_menu)
    else:
        await message.answer("Я тебя не понимаю! Выбери одну из предоставленных опций для оценки этой анкеты:", reply_markup=like_keyboard)
        await state.set_state(Form.like)


async def match_controller(message: types.Message, state: FSMContext):
    """
    Обрабатывает лайк или дизлайк в ответ на входящий лайк
    :param message:
    :param state:
    :return:
    """
    if message.text == "Лайк":
        user = await get_or_create_new_user(chat_id=message.chat.id, change_us=True, username=message.from_user.username)
        data = await state.get_data()
        anket_id = data.get('object_id')
        await delete_likes_between_users(anket_id, message.chat.id)
        anket = await get_or_create_new_user(anket_id)
        if anket.username:
            link = f'https://t.me/{anket.username}'
        else:
            link = f'tg://user?id={anket.id}'
        await message.answer(
            f'<b>Хорошо, у вас взаимный лайк с </b><a href="{link}">{anket.name} (ссылочка на профиль)</a>\n<b>Если ссылка на профиль не работает, проблема в том что пользователь установил такие настройки конфиденциальности</b>',
            parse_mode=ParseMode.HTML
        )

        if user.username:
            link2 = f'https://t.me/{user.username}'
        else:
            link2 = f'tg://user?id={user.id}'
        await message.bot.send_message(chat_id=anket_id,
            text=f'<b>У вас взаимный лайк с </b><a href="{link2}">{user.name} (ссылочка на профиль)</a>\n<b>Если ссылка на профиль не работает, проблема в том что пользователь установил такие настройки конфиденциальности</b>',
            parse_mode=ParseMode.HTML
        )
        data.pop('object_id')
        await state.update_data(**data)
        await message.answer("Выберите дальнейшую опцию:", reply_markup=await get_main_menu_keyboard(await get_likes_count(message.chat.id)))
        await state.set_state(Form.main_menu)
    elif message.text == "Дизлайк":
        data = await state.get_data()
        anket_id = data.get('object_id')
        await delete_likes_between_users(anket_id, message.chat.id)
        data.pop('object_id')
        await state.update_data(**data)
        await message.answer("Окей, выберите дальнейшую опцию:",
                             reply_markup=await get_main_menu_keyboard(await get_likes_count(message.chat.id)))
        await state.set_state(Form.main_menu)
    else:
        await message.answer("Я тебя не понимаю! Выбери одну из предоставленных опций для оценки человека, который тебя лайкнул:", reply_markup=like_keyboard)
        await state.set_state(Form.match)
