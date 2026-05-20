from aiogram.fsm.state import StatesGroup, State


class BookingState(StatesGroup):
    service = State()
    date = State()
    time = State()
    confirm = State()
