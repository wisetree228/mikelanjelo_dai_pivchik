import os
import asyncio
from aiogram import Bot, Dispatcher
from bot.router import main_router

TOKEN = os.getenv('TOKEN')

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('STOPPED')