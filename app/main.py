import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

# Импорты роутеров
from handlers import start, region, user_data, test_generate, book, payment  # <–– добавили payment

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем все роутеры
    dp.include_router(start.router)
    dp.include_router(region.router)
    dp.include_router(user_data.router)
    dp.include_router(test_generate.router)
    dp.include_router(book.router)
    dp.include_router(payment.router)  # <–– подключаем payment

    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
