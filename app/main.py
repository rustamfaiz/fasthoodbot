import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

# Импорт маршрутов
from handlers import start, region, user_data, promocode, test_generate, payment

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры в корректном порядке
    dp.include_router(start.router)
    dp.include_router(region.router)
    dp.include_router(user_data.router)       # 🔥 должен идти раньше всех, кто может перехватить pay_qr
    dp.include_router(promocode.router)
    dp.include_router(test_generate.router)
    dp.include_router(payment.router)

    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
