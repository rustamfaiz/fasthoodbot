from aiogram import Router, types, F
from aiogram.types import CallbackQuery, FSInputFile
from utils.pdf_generator import generate_personal_pdf

router = Router()

@router.callback_query(F.data == "get_book")
async def handle_get_book(callback: CallbackQuery):
    user = callback.from_user
    full_name = user.full_name
    phone = callback.message.chat.id  # или используй реальный, если сохранили

    # Генерация PDF
    output_path = generate_personal_pdf(full_name=full_name, phone=str(phone))

    # Отправка пользователю
    await callback.message.answer_document(
        document=FSInputFile(output_path),
        caption="📘 Вот твоя именная книга. Приятного чтения!"
    )
