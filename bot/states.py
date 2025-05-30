from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    description = State()
    name = State()
    media = State()
    age = State()
    gender = State()