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