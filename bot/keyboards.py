"""
клавиатуры бота
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

choose_gender_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")]
], resize_keyboard=True, one_time_keyboard=True)

choose_gender_keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мужчина", callback_data="man"), InlineKeyboardButton(text="Женщина", callback_data="woman")]
])


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

async def get_main_menu_keyboard_inline(likes_count: int):
    """
    Создаёт клавиатуру для главного меню с указанным количеством входящих лайков
    :param likes_count:
    :return:
    """
    main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Смотреть мою анкету", callback_data="watch_my_anket")],
        [InlineKeyboardButton(text="Листать анкеты", callback_data="watch_ankets")],
        [InlineKeyboardButton(text=f"Входящие лайки: {likes_count}", callback_data="likes")]
    ])
    return main_menu_keyboard


choose_who_you_search = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчин"), KeyboardButton(text="Женщин")],
    [KeyboardButton(text="Кого угодно")]
], resize_keyboard=True, one_time_keyboard=True)

choose_who_you_search_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мужчин", callback_data="search_man"), InlineKeyboardButton(text="Женщин", callback_data="search_woman")],
    [InlineKeyboardButton(text="Кого угодно", callback_data="any")]
])


like_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Лайк"), KeyboardButton(text="Дизлайк")]
], resize_keyboard=True, one_time_keyboard=True)

like_keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Лайк", callback_data="like"), InlineKeyboardButton(text="дизлайк", callback_data="dislike")]
])

change_coordinates_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отказаться")]
], resize_keyboard=True, one_time_keyboard=True)

change_coordinates_keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отказаться", callback_data="cancel")]
])