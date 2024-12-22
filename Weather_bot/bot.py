from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import start, help, weather
from Weather_bot.services import config

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Приветствие"),
        BotCommand(command="/help", description="Список доступных команд"),
        BotCommand(command="/weather", description="Прогноз погоды по маршруту"),
    ]
    await bot.set_my_commands(commands)

async def main():
    await set_commands(bot)
    dp.include_routers(start.router, help.router, weather.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


