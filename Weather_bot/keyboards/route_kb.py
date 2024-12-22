from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def route_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Добавить остановку", callback_data="add_stop"))
    kb.add(InlineKeyboardButton("Подтвердить маршрут", callback_data="confirm_route"))
    return kb
