from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_gender_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")]
], resize_keyboard=True, one_time_keyboard=True)


main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Смотреть мою анкету")],
    [KeyboardButton(text="Листать анкеты")]
], resize_keyboard=True, one_time_keyboard=True)


choose_who_you_search = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчин"), KeyboardButton(text="Женщин")],
    [KeyboardButton(text="Кого угодно")]
], resize_keyboard=True, one_time_keyboard=True)