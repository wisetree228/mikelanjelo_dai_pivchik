"""
клавиатуры бота
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_gender_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")]
], resize_keyboard=True, one_time_keyboard=True)


async def get_main_menu_keyboard(likes_count: int):
    """
    Создаёт клавиатуру для главного меню с указанным количеством входящих лайков
    :param likes_count:
    :return:
    """
    main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Смотреть мою анкету")],
        [KeyboardButton(text="Листать анкеты")],
        [KeyboardButton(text=f"Входящие лайки: {likes_count}")]
    ], resize_keyboard=True, one_time_keyboard=True)
    return main_menu_keyboard


choose_who_you_search = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчин"), KeyboardButton(text="Женщин")],
    [KeyboardButton(text="Кого угодно")]
], resize_keyboard=True, one_time_keyboard=True)


like_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Лайк"), KeyboardButton(text="Дизлайк")]
], resize_keyboard=True, one_time_keyboard=True)

change_coordinates_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отказаться")]
], resize_keyboard=True, one_time_keyboard=True)