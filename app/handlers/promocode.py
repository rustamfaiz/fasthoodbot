from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(lambda c: c.data in ["region_ru", "region_other"])
async def ask_promocode(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Ввести", callback_data="enter_code")
    builder.button(text="Продолжить без кода", callback_data="skip_code")
    builder.button(text="⬅ Назад", callback_data="get_book")
    builder.adjust(1)

    await callback.message.answer(
        "📍 У тебя есть промокод?",
        reply_markup=builder.as_markup()
    )
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Этап после выбора региона
@router.callback_query(lambda c: c.data in ["region_ru", "region_other"])
async def ask_promocode(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(region=callback.data)
    builder = InlineKeyboardBuilder()
    builder.button(text="Ввести", callback_data="enter_code")
    builder.button(text="Продолжить без кода", callback_data="skip_code")
    builder.button(text="⬅ Назад", callback_data="get_book")
    builder.adjust(1)
    await callback.message.answer("📍 У тебя есть промокод?", reply_markup=builder.as_markup())

# Состояния FSM
class PromoStates(StatesGroup):
    waiting_code = State()

# Нажали "Ввести"
@router.callback_query(F.data == "enter_code")
async def ask_code(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("✏️ Введи промокод:")
    await state.set_state(PromoStates.waiting_code)

# Получили промокод
@router.message(PromoStates.waiting_code)
async def process_code(message: types.Message, state: FSMContext):
    code = message.text.strip().lower()
    valid_codes = ["fast100", "rustam50"]  # 🔁 Здесь можно заменить на чтение из БД

    builder = InlineKeyboardBuilder()
    builder.button(text="Продолжить", callback_data="after_code")
    builder.adjust(1)

    if code in valid_codes:
        await state.update_data(promocode=code)
        await message.answer("✅ Код принят. Учтём при расчёте цены.", reply_markup=builder.as_markup())
    else:
        await state.update_data(promocode=None)
        await message.answer("⚠️ Этот код не сработал. Можем идти дальше и без него — я дам тебе эксклюзивную скидку от автора.", reply_markup=builder.as_markup())

    await state.clear()

# "Продолжить без кода"
@router.callback_query(F.data == "skip_code")
async def skip_code(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(promocode=None)
    builder = InlineKeyboardBuilder()
    builder.button(text="Продолжить", callback_data="after_code")
    builder.adjust(1)
    await callback.message.answer("Скидка от меня. Без условий. Без кодов.", reply_markup=builder.as_markup())
