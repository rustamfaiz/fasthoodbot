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
    waiting_for_promocode = State()
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

# Шаг 5 — Россия / ввод промокода
@router.callback_query(F.data == "region_ru")
async def ask_promocode(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.waiting_for_promocode)
    await callback.message.answer("💡 Введи промокод, если он есть. Или напиши «-», чтобы продолжить без него:")

# Шаг 5 — Обработка промокода
@router.message(Form.waiting_for_promocode)
async def handle_promo_and_ask_payment(message: types.Message, state: FSMContext):
    code = message.text.strip()
    promo_applied = False

    if code.lower() == "fat2024":
        await state.update_data(price="2500")
        promo_applied = True
        text = (
            "✅ Промокод активирован! Скидка применена.\n\n"
            "Розничная стоимость книги ФастХуд — Жиросжигание за 4 месяца без голода и беговой дорожки — 3500 рублей\n\n"
            "С твоим промокодом стоимость книги — 2500 рублей"
        )
    elif code == "-":
        await state.update_data(price="2900")
        text = (
            "Ок, промокода нет — не страшно!\n\n"
            "Забирай книгу с личной скидкой от автора:\n"
            "Розничная стоимость книги ФастХуд — Жиросжигание за 4 месяца без голода и беговой дорожки — 3500 рублей\n\n"
            "Цена для тебя — 2900 рублей"
        )
    else:
        await message.answer(
            "❌ Такого промокода нет.\n"
            "Проверь ещё раз или напиши «-», чтобы продолжить без него — с личной скидкой от автора."
        )
        return

    await message.answer(text)

    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Оплатить через СБП", callback_data="pay_qr")
    builder.button(text="⚠️ Оплатить через ЮKassa", callback_data="pay_yookassa")
    builder.button(text="⬅ Назад", callback_data="back_to_promocode")
    builder.adjust(1)

    await message.answer(
        "Выбери удобный способ оплаты:\n\n"
        "📌 Через СБП — отправка книги в течение 24 часов\n"
        "📌 Через ЮKassa — автоматическая генерация за 15 минут (в разработке)",
        reply_markup=builder.as_markup()
    )

# Обработка кнопки ЮKassa (временно не работает)
@router.callback_query(F.data == "pay_yookassa")
async def temp_yookassa_notice(callback: types.CallbackQuery):
    await callback.message.answer(
        "❌ Этот способ оплаты пока в разработке.\n"
        "Выбери другой способ."
    )

# Обработка кнопки Назад к промокоду
@router.callback_query(F.data == "back_to_promocode")
async def back_to_promo(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.waiting_for_promocode)
    await callback.message.answer("🔁 Введи промокод ещё раз или напиши «-», если его нет:")

# Заглушка для СБП (временно): обработка pay_qr — сюда пойдём в следующем шаге
@router.callback_query(F.data == "pay_qr")
async def handle_qr_payment(callback: types.CallbackQuery):
    await callback.message.answer("🧾 Переход к оплате через СБП... (в разработке)")
