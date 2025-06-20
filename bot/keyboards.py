"""
клавиатуры бота
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

choose_gender_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")]
], resize_keyboard=True, one_time_keyboard=True)


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


like_keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Лайк", callback_data="like"), InlineKeyboardButton(text="дизлайк", callback_data="dislike")]
])

like_keyboard_match_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Лайк", callback_data="like_match"), InlineKeyboardButton(text="дизлайк", callback_data="dislike_match")]
])

change_coordinates_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отказаться")]
], resize_keyboard=True, one_time_keyboard=True)
