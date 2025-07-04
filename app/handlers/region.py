from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

from app.utils.pdf_generator import generate_personal_pdf
import os

router = Router()

# Шаг 4 — Выбор региона
@router.callback_query(lambda c: c.data == "get_book")
async def ask_region(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Россия", callback_data="region_ru")
    builder.button(text="Другие страны", callback_data="region_other")
    builder.button(text="⬅ Назад", callback_data="back_to_start")
    builder.adjust(1)

    await callback.message.answer(
        "📍 Укажи регион — для определения способа оплаты:",
        reply_markup=builder.as_markup()
    )

# Шаг 5.1 — Оплата для России
@router.callback_query(lambda c: c.data == "region_ru")
async def handle_russia(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Я оплатил", callback_data="paid_russia")
    builder.adjust(1)

    await callback.message.answer(
        "💳 <b>Оплата</b>\n"
        "Чтобы получить книгу, перейди по ссылке и оплати заказ:\n"
        "🔗 <a href='https://example.com/pay_russia'>ОПЛАТИТЬ</a>\n\n"
        "После оплаты нажми «Я оплатил» — и мы пришлём тебе именной файл.",
        reply_markup=builder.as_markup(),
        disable_web_page_preview=True
    )

# Шаг 5.2 — Оплата для других стран
@router.callback_query(lambda c: c.data == "some_value")

