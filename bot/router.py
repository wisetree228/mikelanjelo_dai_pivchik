from aiogram import Router
from aiogram.filters import CommandStart
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