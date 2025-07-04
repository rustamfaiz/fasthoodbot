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
