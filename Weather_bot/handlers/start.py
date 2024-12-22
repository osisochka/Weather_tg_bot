from aiogram import Router, types
from aiogram.filters.command import Command

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот прогноза погоды. Введите /help для списка команд.")
