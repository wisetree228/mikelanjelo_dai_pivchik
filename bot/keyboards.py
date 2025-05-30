from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_gender_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")]
], resize_keyboard=False)


main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Смотреть мою анкету")],
    [KeyboardButton(text="Кнопка 2")]
])