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
@router.callback_query(lambda c: c.data == "region_other")
async def handle_other_countries(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ I Paid", callback_data="paid_other")
    builder.adjust(1)

    await callback.message.answer(
        "💳 <b>Payment</b>\n"
        "To get the book, please pay via the link below:\n"
        "🔗 <a href='https://example.com/pay_world'>PAY NOW</a>\n\n"
        "Once paid, click 'I Paid' and we’ll send you your personal file.",
        reply_markup=builder.as_markup(),
        disable_web_page_preview=True
    )

# Шаг 6 — Подтверждение оплаты (временно без PDF)
@router.callback_query(lambda c: c.data.startswith("paid_"))
async def handle_payment_confirmation(callback: types.CallbackQuery):
    await callback.message.answer(
        "🔧 Спасибо! Оплата подтверждена (в тестовом режиме).\n"
        "Скоро пришлём твою именную книгу."
    )

