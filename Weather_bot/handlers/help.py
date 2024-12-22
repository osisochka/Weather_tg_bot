from aiogram import Router, types
from aiogram.filters.command import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "/start - Приветствие\n"
        "/help - Список команд\n"
        "/weather - Прогноз погоды для маршрута"
    )
