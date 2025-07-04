from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.pdf_generator import generate_personal_pdf

router = Router()

class PaymentFSM(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_phone = State()

# Шаг 6.1 — после нажатия "✅ Я оплатил"
@router.callback_query(F.data.startswith("paid_"))
async def handle_payment_confirmation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📝 Введи своё <b>ФИО</b>, чтобы мы подписали книгу.")
    await state.set_state(PaymentFSM.waiting_for_full_name)

# Шаг 6.2 — получаем ФИО
@router.message(PaymentFSM.waiting_for_full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer("📱 Теперь введи номер телефона (в международном формате).")
    await state.set_state(PaymentFSM.waiting_for_phone)

# Шаг 6.3 — получаем телефон, генерируем PDF и отправляем
@router.message(PaymentFSM.waiting_for_phone)
async def get_phone_and_send_pdf(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    full_name = user_data.get("full_name")
    phone = message.text.strip()

    input_path = "files/тест книги.pdf"
    output_path = f"files/book_{message.from_user.id}.pdf"

    generate_personal_pdf(
        input_path=input_path,
        output_path=output_path,
        full_name=full_name,
        phone_number=phone
    )

    await message.answer_document(
        types.FSInputFile(path=output_path),
        caption="📘 Готово! Вот твоя именная книга."
    )
    await state.clear()
