from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "test_send_pdf")
async def send_test_pdf(callback: types.CallbackQuery):
    await callback.message.answer_document(
        types.FSInputFile("files/тест книги.pdf"),
        caption="🧪 Это тестовая генерация PDF.\nФайл успешно отправлен."
    )
