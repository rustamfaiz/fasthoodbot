# Шаг 5.2 — Оплата для других стран
@router.callback_query(lambda c: c.data == "region_other")
async def handle_other_country(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Назад", callback_data="get_book")
    builder.adjust(1)

    await callback.message.answer(
        "🌍 Направление в разработке. Скоро запустимся.",
        reply_markup=builder.as_markup()
    )
