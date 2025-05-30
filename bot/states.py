from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    description = State()
    name = State()
    avatar = State()
    age = State()
    gender = State()