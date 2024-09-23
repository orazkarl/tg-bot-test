import asyncio

from aiogram import Bot, Dispatcher

from config import API_TOKEN
from handlers import router

bot = Bot(token=API_TOKEN)
dp = Dispatcher()



async def main():
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
