from aiogram import Router, types, F
from aiogram.types import CallbackQuery, FSInputFile
from utils.pdf_generator import generate_personal_pdf

router = Router()

@router.callback_query(F.data == "get_book")
async def handle_get_book(callback: CallbackQuery):
    user = callback.from_user
    full_name = user.full_name
    phone = str(callback.message.chat.id)  # или реальный, если есть

    # Пути к файлам
    input_path = "files/тест книги.pdf"
    output_path = f"files/book_{user.id}.pdf"

    # Генерация PDF
    generate_personal_pdf(input_path, output_path, full_name, phone)

    # Отправка пользователю
    await callback.message.answer_document(
        document=FSInputFile(output_path),
        caption="📘 Вот твоя именная книга. Приятного чтения!"
    )
