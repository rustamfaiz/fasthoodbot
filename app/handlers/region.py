from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

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
