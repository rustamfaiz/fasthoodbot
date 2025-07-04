from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(lambda c: c.data in ["region_ru", "region_other"])
async def ask_promocode(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Ввести", callback_data="enter_code")
    builder.button(text="Продолжить без кода", callback_data="skip_code")
    builder.button(text="⬅ Назад", callback_data="get_book")
    builder.adjust(1)

    await callback.message.answer(
        "📍 У тебя есть промокод?",
        reply_markup=builder.as_markup()
    )
