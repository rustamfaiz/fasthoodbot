from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.pdf_generator import generate_personal_pdf

ADMIN_ID = 335067126  # Telegram ID админа

router = Router()

# Временное хранилище данных пользователя
user_data_dict = {}

class Form(StatesGroup):
    waiting_for_payment_screenshot = State()
    waiting_for_name = State()
    waiting_for_phone = State()

# 🟢 Шаг 1 — пользователь нажал «Я оплатил»
@router.callback_query(F.data == "confirm_payment_started")
async def ask_payment_proof(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🧾 Пришли, пожалуйста, скриншот чека об оплате — или фото из приложения.\n\n"
        "Так мы быстрее подтвердим платёж и подготовим твою книгу."
    )
    await state.set_state(Form.waiting_for_payment_screenshot)

# 🟢 Шаг 2 — получил скрин → просим ФИО
@router.message(Form.waiting_for_payment_screenshot, F.photo)
async def ask_full_name(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(screenshot_file_id=file_id)

    await message.answer("📝 Введи своё **ФИО** — так мы сделаем книгу именной.", parse_mode="Markdown")
    await state.set_state(Form.waiting_for_name)

# 🔴 если не фото — просим фото
@router.message(Form.waiting_for_payment_screenshot)
async def invalid_payment_format(message: Message):
    await message.answer("❗ Пожалуйста, пришли изображение — фото или скриншот чека.")

# 🟢 Шаг 3 — получил ФИО → просим телефон
@router.message(Form.waiting_for_name)
async def ask_phone(message: Message, state: FSMContext):
    full_name = message.text.strip()
    if len(full_name.split()) < 2:
        await message.answer("❗ Пожалуйста, введи имя и фамилию — например: `Иван Петров`", parse_mode="Markdown")
        return

    await state.update_data(name=full_name)
    await message.answer("📞 Теперь введи **номер телефона** — чтобы мы могли связаться при необходимости.\n\nФормат: +79001234567", parse_mode="Markdown")
    await state.set_state(Form.waiting_for_phone)

# 🟢 Шаг 4 — получил телефон → отправляем админу
@router.message(Form.waiting_for_phone)
async def send_to_admin(message: Message, state: FSMContext):
    phone = message.text.strip()

    if not phone.startswith("+") or not phone[1:].isdigit() or len(phone) < 11:
        await message.answer("❗ Введи корректный номер телефона в формате +79001234567")
        return

    await state.update_data(phone=phone)
    data = await state.get_data()

    name = data.get("name", "Не указано")
    screenshot_file_id = data.get("screenshot_file_id")
    username = message.from_user.username or "—"
    user_id = message.from_user.id

    # Сохраняем данные во временный словарь
    user_data_dict[user_id] = {
        "name": name,
        "phone": phone
    }

    # Кнопка для админа
    builder = InlineKeyboardBuilder()
    builder.button(text="📘 Подтвердить и отправить книгу", callback_data=f"confirm_payment:{user_id}")
    builder.adjust(1)

    # Сообщение админу
    caption = (
        f"🆕 Новый платёж\n\n"
        f"👤 ФИО: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"🔗 Telegram: @{username}\n"
        f"🖼 Чек во вложении"
    )

    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=screenshot_file_id,
        caption=caption,
        reply_markup=builder.as_markup()
    )

    await message.answer(
        "✅ Спасибо! Все данные получены.\n\n"
        "📘 В течение 24 часов тебе будет сгенерирована именная версия книги. "
        "Она придёт прямо сюда, в этот чат.\n\n"
        "Ожидай. Всё идёт по плану."
    )

    await state.clear()

# 🟢 Шаг 5 — админ подтверждает → бот отправляет книгу
@router.callback_query(F.data.startswith("confirm_payment:"))
async def confirm_payment(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Только админ может подтверждать оплату.", show_alert=True)
        return

    user_id = int(callback.data.split(":")[1])
    user_data = user_data_dict.get(user_id, {})
    name = user_data.get("name", "Покупатель")
    phone = user_data.get("phone", "Не указан")

    pdf_path = generate_personal_pdf(name=name, phone=phone)
    pdf = FSInputFile(pdf_path)

    await callback.message.bot.send_document(
        chat_id=user_id,
        document=pdf,
        caption="📘 Вот твоя книга. Удачи!"
    )
    await callback.answer("✅ Книга отправлена.")
    # 🔁 Обработчик кнопки оплаты через СБП (QR)
@router.callback_query(F.data == "pay_qr")
async def show_qr(callback: types.CallbackQuery, state: FSMContext):
    photo = FSInputFile("files/qr.png")
    data = await state.get_data()
    price = data.get("price", "2900")

    await callback.message.answer_photo(photo)

    await callback.message.answer(
        f"📲 Готово к оплате.\n\n"
        f"Чтобы оплатить книгу, просто:\n"
        f"— Отсканируй QR-код выше камерой телефона\n"
        f"или\n"
        f"— <a href='https://www.tinkoff.ru/rm/r_rPnohUIkbB.eRVktSOsDc/3Ioud12615'>Перейди по ссылке и оплати</a> картой или через СБП\n\n"
        f"💳 Стоимость: {price} рублей\n\n"
        f"После оплаты нажми кнопку «✅ Я оплатил»",
        parse_mode="HTML"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Я оплатил", callback_data="confirm_payment_started")
    builder.adjust(1)
    await callback.message.answer("Когда оплатишь — нажми кнопку:", reply_markup=builder.as_markup())

