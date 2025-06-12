"""
Состояния обработки бота
"""
from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    """
    Состояния обработки для бота
    """
    description = State()
    name = State()
    media = State()
    age = State()
    gender = State()
    main_menu = State()
    who_search = State()
    like = State()
    match = State()
    coordinates = State()
    city = State()