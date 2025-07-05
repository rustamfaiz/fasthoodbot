from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.pdf_generator import generate_personal_pdf

import os

router = Router()

# Состояния
class Form(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_payment = State()

# ID админа
ADMIN_ID = 335067126

# Путь к QR-коду
QR_IMAGE_PATH = "files/qr.png"

@router.message(F.text == "✅ Я оплатил")
async def ask_payment_screenshot(message: types.Message, state: FSMContext):
    await message.answer("📸 Пришли скриншот с оплатой")
    await state.set_state(Form.waiting_for_payment)

@router.message(Form.waiting_for_payment, F.photo)
async def handle_payment_screenshot(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or "неизвестен"
    photo = message.photo[-1]
    file_id = photo.file_id

    # Отправка админу
    builder = InlineKeyboardBuilder()
    builder.button(text="📘 Подтвердить и отправить книгу", callback_data=f"confirm_payment:{user_id}")
    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=file_id,
        caption=f"🧾 Оплата от пользователя @{username} (ID: {user_id})",
        reply_markup=builder.as_markup()
    )

    await message.answer("✅ Спасибо. Ожидай подтверждения оплаты.")

@router.callback_query(F.data.startswith("confirm_payment:"))
async def confirm_payment(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Только админ может подтверждать оплату.", show_alert=True)
        return

    user_id = int(callback.data.split(":")[1])

    # Генерация PDF
    pdf_path = generate_personal_pdf(name="Покупатель", phone="Не указан")
    pdf = FSInputFile(pdf_path)

    await callback.message.bot.send_document(
        chat_id=user_id,
        document=pdf,
        caption="📘 Вот твоя книга. Удачи!"
    )
    await callback.answer("✅ Книга отправлена.")
