from Weather_bot.services.weather_services import get_forecast_for_route
from aiogram import Router, types
from aiogram.filters.command import Command


router = Router()

@router.message(Command("weather"))
async def weather_command(message: types.Message):
    await message.answer("Введите начальную точку маршрута (через запятую):")

@router.message()
async def route_input(message: types.Message):
    route_points = message.text.split()
    if len(route_points) < 2:
        await message.answer("Ошибка: укажите хотя бы начальную и конечную точки (например, Москва, Санкт-Петербург).")
        return

    forecast = get_forecast_for_route(route_points)
    await message.answer(forecast)

