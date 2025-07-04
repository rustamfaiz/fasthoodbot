import asyncio
from aiogram import Router, types, Bot
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="💸 Получить книгу", callback_data="get_book")
    builder.button(text="🎯 Что ты получишь из этой книги", callback_data="about_book")
    builder.adjust(1)

    text = (
        "🎯 <b>Поздравляю.</b>\n"
        "Новая попытка. Новый заход. Очередной старт против жира, который всё ещё с тобой.\n\n"
        "— — — — — — — — — — —\n\n"
        "Давай честно — у тебя уже были диеты, был бег, была надежда увидеть плоский живот — хотя бы один раз, без возврата.\n"
        "Но вместо результата — снова цифры туда-сюда. И снова ничего.\n\n"
        "— — — — — — — — — — —\n\n"
        "👋 Привет. Меня зовут Рустам.\n"
        "В 2019 году я сжёг двадцать килограммов — через голод, бег, полное отречение от сладкого, мучного и жизни.\n\n"
        "Настолько ушёл в процесс, что разобрал физиологию, нутрициологию и тренировочную механику до костей.\n"
        "Потом специально набирал жир — и сжигал его снова. Несколько раз.\n"
        "Системно. Без голода, без бега и со вкусом жизни. За 4 месяца.\n\n"
        "Так и появилась эта книга.\n"
        "Не из вдохновения. А из проверенной практики в борьбе с фитнес-мифами и бесполезными ритуалами.\n\n"
        "🚫 Это не про мотивацию. Это про метод.\n"
        "🔥 Как за 4 месяца убрать жир — и не вернуть его больше никогда.\n\n"
        "⬇️ Жми кнопку — и получи свою книгу."
    )

    await message.answer(text, reply_markup=builder.as_markup(), disable_web_page_preview=True)

@router.callback_query(lambda c: c.data == "about_book")
async def about_book(callback: types.CallbackQuery, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.button(text="🔴 Получить книгу", callback_data="get_book")
    builder.button(text="🔵 Вернуться", callback_data="back_to_start")
    builder.adjust(1)

    text = (
        "Это не книга. Это прямой удар по всем фитнес-мифам, на которых ты сливал годы.\n"
        "Без мотивационных соплей, без “всё получится”, без брокколи на пару.\n\n"
        "Здесь — метод.\n"
        "4 месяца. Без голода. Без бега. Без возврата жира.\n\n"
        "Вот что ты получаешь:\n"
        "▪️ Пошаговый план жиросжигания, собранный по физиологии, а не по мнению тренеров\n"
        "▪️ Программа питания, где есть мясо, хлеб, нормальные продукты — и при этом жир уходит\n"
        "▪️ Полная система тренировок — три фазы, весь зал, расписано по неделям\n"
        "▪️ Разбор, почему диеты всегда проваливаются — и как не повторить ту же яму\n"
        "▪️ Честный ответ, почему “ПП” не работает, и что работает вместо\n"
        "▪️ Формулу удержания формы — чтобы не набрать обратно, даже если жизнь снова начнёт валиться\n"
        "▪️ Понимание тела — как оно реально тратит жир, что делает инсулин, и как управлять аппетитом\n"
        "▪️ Новое тело. Реально. За 4 месяца. Без воды. Без отката. Без иллюзий."
    )

    await callback.message.edit_text(text, disable_web_page_preview=True)
    await asyncio.sleep(5)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo="https://i.imgur.com/jX4pQcI.jpeg",
        reply_markup=builder.as_markup()
    )

@router.callback_query(lambda c: c.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    await start_handler(callback.message)

@router.callback_query(lambda c: c.data == "get_book")
async def get_book(callback: types.CallbackQuery):
    await callback.message.answer("⏳ Раздел в разработке. Скоро продолжим.")
