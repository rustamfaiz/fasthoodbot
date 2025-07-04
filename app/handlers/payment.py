from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from utils.pdf_generator import generate_personal_pdf

import random
import os

router = Router()

# Состояния для FSM
class Form(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()

# Шаг 4 — Выбор региона
@router.callback_query(F.data == "get_book")
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
@router.callback_query(F.data == "region_ru")
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
@router.callback_query(F.data == "region_other")
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

# Шаг 6 — После оплаты (ввод ФИО)
@router.callback_query(F.data.startswith("paid_"))
async def ask_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.waiting_for_name)
    await callback.message.answer("✍️ Введи ФИО (для подписи в книге):")

# Шаг 7 — Получили имя, спрашиваем телефон
@router.message(Form.waiting_for_name)
async def ask_phone(message: types.Message, state: FSMContext):
    print("📝 Получено ФИО:", message.text)  # лог в консоль
    await state.update_data(full_name=message.text)
    await state.set_state(Form.waiting_for_phone)
    await message.answer("📞 Введи номер телефона (будет виден только тебе):")

# Шаг 8 — Получили телефон, генерируем PDF
@router.message(Form.waiting_for_phone)
async def generate_and_send(message: types.Message, state: FSMContext):
    print("⚙️ generate_and_send START")  # лог в консоль

    try:
        data = await state.get_data()
        full_name = data.get("full_name", "Имя неизвестно")
        phone = message.text

        print(f"📩 Телефон получен: {phone}")
        print(f"👤 Имя в state: {full_name}")

        await message.answer("📚 Генерируем твою именную книгу...")

        # Пути к файлам
        input_path = "files/тест книги.pdf"
        output_path = f"files/generated_{random.randint(1000, 9999)}.pdf"

        # Генерация PDF
        pdf_path = generate_personal_pdf(input_path, output_path, full_name, phone)

        # Проверка файла
        if pdf_path and os.path.exists(pdf_path):
            print(f"✅ PDF создан: {pdf_path}")
            await message.answer_document(FSInputFile(pdf_path))
            await message.answer(
                "✅ Готово!\n"
                "Это твоя именная книга. Читай, применяй — и сожги весь жир за 4 месяца.\n\n"
                "📌 Это персональный файл. Дарить можно только друзьям. Лучше делись своим промокодом и получай бонусы.\n"
                "Присылай фото в новом теле и отмечай @rustam_faiz 😉"
            )
        else:
            print("❌ PDF не найден")
            await message.answer("❌ Ошибка: файл не найден. Напиши @rustam_faiz.")

    except Exception as e:
        print(f"❌ Ошибка generate_and_send: {e}")
        await message.answer(f"❌ Произошла ошибка при генерации: {e}")

    await state.clear()
