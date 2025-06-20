"""
Роуты (обработчики состояний) бота
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from bot.command_controllers import *
from bot.states import Form
from aiogram.fsm.context import FSMContext
from aiogram import types

main_router = Router()

@main_router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /start
    """
    return await start_controller(message, state)


@main_router.message(Form.name)
async def handle_set_name(message: types.Message, state: FSMContext):
    """
    Обрабатывает смену имени
    """
    return await set_name_controller(message, state)


@main_router.message(Form.age)
async def handle_set_age(message: types.Message, state: FSMContext):
    """
    Обрабатывает смену возраста
    """
    return await set_age_controller(message, state)


@main_router.message(Form.gender)
async def handle_set_gender(message: types.Message, state: FSMContext):
    """
    Обрабатывает смену пола в анкете
    """
    return await set_gender_controller(message, state)


@main_router.message(Form.description)
async def handle_set_description(message: types.Message, state: FSMContext):
    """
    Обрабатывает смену описания в анкете
    """
    return await set_description_controller(message, state)


@main_router.message(Command(commands=['edit']))
async def handle_edit_profile(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /edit (редактирование профиля)
    """
    return await edit_profile_controller(message, state)


@main_router.message(Form.media)
async def handle_edit_media(message: types.Message, state: FSMContext):
    """
    Обрабатывает смену медиафайлов
    """
    return await edit_media_controller(message, state)


@main_router.message(Form.coordinates)
async def handle_change_location(message: types.Message, state: FSMContext):
    """
    Обрабатывает смену геолокации
    """
    return await change_location_controller(message, state)


@main_router.message(Form.city)
async def handle_edit_city(message: types.Message, state: FSMContext):
    """
    Обрабатывает смену города
    """
    return await edit_city_controller(message, state)


@main_router.callback_query(F.data=='watch_my_anket')
async def handle_watch_anket(callback: types.CallbackQuery, state: FSMContext):
    """
    Просмотр своей анкеты
    """
    return await watch_my_anket_controller(callback, state)


@main_router.callback_query(F.data=='watch_ankets')
async def handle_watch_ankets(callback: types.CallbackQuery, state: FSMContext):
    """
    Листание анкет
    """
    return await watch_ankets_controller(callback, state)


@main_router.callback_query(F.data=='like')
async def handle_like_inline(callback: types.CallbackQuery, state: FSMContext):
    """
    Обработчик лайка
    """
    return await like_controller_inline(callback, state)


@main_router.callback_query(F.data=='dislike')
async def handle_dislike_inline(callback: types.CallbackQuery, state: FSMContext):
    """
    Обработчик дизлайка
    """
    return await dislike_controller_inline(callback, state)


@main_router.callback_query(F.data=='likes')
async def handle_likes_inline(callback: types.CallbackQuery, state: FSMContext):
    """
    Просмотр входящих лайков
    """
    return await likes_controller_inline(callback, state)


@main_router.callback_query(F.data=='like_match')
async def handle_like_match_inline(callback: types.CallbackQuery, state: FSMContext):
    """
    Ответный лайк на входящий лайк
    """
    return await like_match_controller_inline(callback, state)


@main_router.callback_query(F.data=='dislike_match')
async def handle_dislike_match_inline(callback: types.CallbackQuery, state: FSMContext):
    """
    Дизлайк на входящий лайк
    """
    return await dislike_match_controller_inline(callback, state)


@main_router.message(Form.who_search)
async def handle_who_search(message: types.Message, state: FSMContext):
    """
    Обрабатывает смену того, чьи анкеты интересны пользователю
    """
    return await who_search_controller(message, state)
