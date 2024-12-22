from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Weather_bot.services.weather_services import get_forecast_for_route

router = Router()

# Глобальная переменная для хранения временного интервала
TIME_INTERVAL = {"days": 3}  # По умолчанию 3 дня


def get_time_interval_keyboard():
    """Создает клавиатуру для выбора временного интервала."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="на 1 день", callback_data="interval:1"),
            InlineKeyboardButton(text="на 3 дня", callback_data="interval:3"),
            InlineKeyboardButton(text="на 5 дней", callback_data="interval:5"),
        ]
    ])
    return keyboard


@router.message(Command("weather"))
async def weather_command(message: types.Message):
    """Команда для начала процесса выбора маршрута."""
    await message.answer(
        "Введите начальную и конечную точки маршрута через запятую. \nНапример:\nМосква, Санкт-Петербург\n\n Выберите интервал прогноза",
        reply_markup=get_time_interval_keyboard(),
    )


@router.message()
async def route_input(message: types.Message):
    """Обработка маршрута."""
    route_points = message.text.split()
    if len(route_points) < 2:
        await message.answer(
            "Ошибка: укажите хотя бы начальную и конечную точки (например, Москва, Санкт-Петербург)."
        )
        return

    forecast = get_forecast_for_route(route_points, days=TIME_INTERVAL["days"])
    await message.answer(forecast)


@router.callback_query()
async def handle_time_interval(callback: types.CallbackQuery):
    """Обработка выбора временного интервала через инлайн-кнопки."""
    if callback.data.startswith("interval:"):
        interval = int(callback.data.split(":")[1])
        TIME_INTERVAL["days"] = interval
        await callback.message.answer(f"Вы выбрали прогноз на {interval} {'день' if interval == 1 else 'дня' if interval in [2, 3, 4] else 'дней'}.")
        await callback.answer()



