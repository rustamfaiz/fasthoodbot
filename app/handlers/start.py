from aiogram import Router, types
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

