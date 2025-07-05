from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.pdf_generator import generate_personal_pdf

ADMIN_ID = 335067126  # Telegram ID админа

router = Router()

class Form(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_payment_screenshot = State()

# 🟢 Обработчик кнопки СБП (QR)
@router.callback_query(F.data == "pay_qr")
async def show_qr(callback: types.CallbackQuery, state: FSMContext):
    photo = FSInputFile("files/qr.png")
    await callback.message.answer_photo(photo)

    data = await state.get_data()
    price = data.get("price", "2900")

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

# 🔁 После нажатия «Я оплатил»
@router.callback_query(F.data == "confirm_payment_started")
async def ask_payment_proof(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🧾 Пришли, пожалуйста, скриншот чека об оплате — или фото из приложения.\n\n"
        "Так мы быстрее подтвердим платёж и подготовим твою книгу."
    )
    await state.set_state(Form.waiting_for_payment_screenshot)

# 📥 Приём скрина оплаты
@router.message(Form.waiting_for_payment_screenshot, F.photo)
async def handle_payment_screenshot(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "Не указано")
    phone = data.get("phone", "Не указан")
    price = data.get("price", "2900")
    user_id = message.from_user.id
    username = message.from_user.username or "—"

    # Кнопка админа
    builder = InlineKeyboardBuilder()
    builder.button(text="📘 Подтвердить и отправить книгу", callback_data=f"confirm_payment:{user_id}")
    builder.adjust(1)

    # Отправка админу
    caption = (
        f"🆕 Новый платёж через СБП\n\n"
        f"👤 ФИО: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"💳 Сумма: {price} ₽\n"
        f"🔗 Telegram: @{username}\n"
        f"🖼 Чек во вложении"
    )
    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=caption,
        reply_markup=builder.as_markup()
    )

    await message.answer(
        "✅ Спасибо! Оплата получена.\n\n"
        "📘 В течение 24 часов тебе будет сгенерирована именная версия книги. "
        "Она придёт прямо сюда, в этот чат.\n\n"
        "Ожидай. Всё идёт по плану."
    )
    await state.clear()

# ❗ Если не фото
@router.message(Form.waiting_for_payment_screenshot)
async def invalid_payment_format(message: types.Message):
    await message.answer("❗ Пожалуйста, пришли изображение — фото или скриншот чека.")

# ✅ Обработка подтверждения оплаты админом
@router.callback_query(F.data.startswith("confirm_payment:"))
async def confirm_payment(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Только админ может подтверждать оплату.", show_alert=True)
        return

    user_id = int(callback.data.split(":")[1])
    pdf_path = generate_personal_pdf(name="Покупатель", phone="Не указан")
    pdf = FSInputFile(pdf_path)

    await callback.message.bot.send_document(
        chat_id=user_id,
        document=pdf,
        caption="📘 Вот твоя книга. Удачи!"
    )
    await callback.answer("✅ Книга отправлена.")
