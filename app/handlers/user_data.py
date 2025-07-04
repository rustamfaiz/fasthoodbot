from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

class UserData(StatesGroup):
    waiting_for_name = State()
    waiting_for_email = State()

@router.callback_query(lambda c: c.data == "pay_card")
async def start_user_data(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("✍️ Введи своё <b>имя</b>, чтобы оно появилось на обложке книги:")
    await state.set_state(UserData.waiting_for_name)

@router.message(UserData.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📧 Теперь введи <b>email</b> — на случай, если понадобится связаться:")
    await state.set_state(UserData.waiting_for_email)

@router.message(UserData.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()

    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Перейти к оплате",
        url="https://example.com/pay"  # ← позже заменим на настоящую ссылку
    )
    builder.adjust(1)

    await message.answer(
        f"🎉 Отлично! Вот что ты ввёл:\n\n"
        f"👤 Имя: <b>{data['name']}</b>\n"
        f"📧 Email: <b>{data['email']}</b>\n\n"
        f"Теперь жми кнопку ниже — и переходи к оплате:",
        reply_markup=builder.as_markup()
    )

    await state.clear()
