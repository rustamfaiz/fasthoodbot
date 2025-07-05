# handlers/region.py

from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

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

# Шаг 5.2 — Оплата для других стран (заглушка)
@router.callback_query(lambda c: c.data == "region_other")
async def handle_other_country(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Назад", callback_data="get_book")
    builder.adjust(1)

    await callback.message.answer(
        "🌍 Пока доступна только оплата для России.\n"
        "Скоро подключим международные платежи.",
        reply_markup=builder.as_markup()
    )
