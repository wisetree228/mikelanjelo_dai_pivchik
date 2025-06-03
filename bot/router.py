from aiogram import Router
from aiogram.filters import CommandStart, Command
from bot.command_controllers import *
from bot.states import Form
from aiogram.fsm.context import FSMContext
from aiogram import types

main_router = Router()

@main_router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    return await start_controller(message, state)


@main_router.message(Form.name)
async def handle_set_name(message: types.Message, state: FSMContext):
    return await set_name_controller(message, state)


@main_router.message(Form.age)
async def handle_set_age(message: types.Message, state: FSMContext):
    return await set_age_controller(message, state)


@main_router.message(Form.gender)
async def handle_set_gender(message: types.Message, state: FSMContext):
    return await set_gender_controller(message, state)


@main_router.message(Form.description)
async def handle_set_gender(message: types.Message, state: FSMContext):
    return await set_description_controller(message, state)


@main_router.message(Command(commands=['edit']))
async def handle_edit_profile(message: types.Message, state: FSMContext):
    return await edit_profile_controller(message, state)


@main_router.message(Form.media)
async def handle_edit_media(message: types.Message, state: FSMContext):
    return await edit_media_controller(message, state)


@main_router.message(Form.main_menu)
async def handle_main_menu(message: types.Message, state: FSMContext):
    return await main_menu_controller(message, state)


@main_router.message(Form.who_search)
async def handle_who_search(message: types.Message, state: FSMContext):
    return await who_search_controller(message, state)


@main_router.message(Form.like)
async def handle_like(message: types.Message, state: FSMContext):
    return await like_controller(message, state)


@main_router.message(Form.match)
async def handle_match(message: types.Message, state: FSMContext):
    return await match_controller(message, state)