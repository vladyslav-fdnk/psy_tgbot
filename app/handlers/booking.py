from aiogram import Router, F
from aiogram.types import Message, CallbackQuery,  InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

router = Router()


def get_time_keyboard():
    time_slots = [
        "10:30",
        "12:00",
        "13:30",
        "14:30",
        "15:00",
        "16:30"
    ]

    keybord = []

    for slot in time_slots:
        keybord.append([
            InlineKeyboardButton(
                text=slot,
                callback_data=f"time_{slot}"
            )
        ])
    return InlineKeyboardMarkup(
        inline_keyboard=keybord
    )


@router.message(F.text == "/booking")
async def booking(message: Message):
    await message.answer(
        "Выберите дату консультации 📅",
        reply_markup=await SimpleCalendar().start_calendar()
    )


@router.callback_query(SimpleCalendarCallback.filter())
async def process_calendar(
    callback: CallbackQuery,
    callback_data: SimpleCalendarCallback,
):
    selected, date = await SimpleCalendar().process_selection(
        callback,
        callback_data
    )

    if selected:
        date = date.strftime('%Y-%m-%d')
        await callback.message.answer(
            f"Вы выбрали дату: {date}\nТеперь выберите время:",
            reply_markup=get_time_keyboard()
        )

@router.callback_query(F.data.startswith(f"time_"))
async def process_time_(callback: CallbackQuery):
    time = callback.data.replace("time_", "")
    await callback.message.answer(
        f'Ваш выбор: {date}, {time}\n'
        f'Ожидайте подтверждения даты'
    )
    await callback.answer()