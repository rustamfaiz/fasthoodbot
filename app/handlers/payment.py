from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(lambda c: c.data in ["region_ru", "region_other"])
async def choose_payment(callback: types.CallbackQuery):
    region = "🇷🇺 Россия" if callback.data == "region_ru" else "🌍 Другие страны"

    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Оплатить картой", callback_data="pay_card")
    builder.button(text="⬅ Назад", callback_data="get_book")
    builder.adjust(1)

    await callback.message.answer(
        f"✅ Регион: <b>{region}</b>\n\n"
        f"Цена книги: <b>490 ₽</b> (около $5)\n"
        f"Выберите способ оплаты:",
        reply_markup=builder.as_markup()
    )
from aiogram import Router, types
from aiogram.types import FSInputFile

router = Router()

@router.callback_query(lambda c: c.data == "payment_success")
async def send_pdf(callback: types.CallbackQuery):
    file_path = "files/тест книги.pdf"  # путь к тестовой PDF-книге

    document = FSInputFile(file_path, filename="FastHood_Тест.pdf")

    await callback.message.answer_document(document)
    await callback.message.answer(
        "📘 Готово! Вот твоя книга.\n\n"
        "Если хочешь поделиться результатом — присылай фото тела до/после и отмечай @rustam_faiz 🏋️‍♂️"
    )
