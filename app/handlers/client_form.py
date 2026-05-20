from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.database.db import save_client, ClientData

router = Router()


class ClientForm(StatesGroup):
    name = State()
    age = State()
    timezone = State()
    request = State()
    therapy = State()
    anxiety = State()
    contact = State()


@router.callback_query(F.data == "fill_form")
async def fill_form(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    if not callback.message:
        return

    await callback.answer()

    await callback.message.answer("Как вас зовут?")
    await state.set_state(ClientForm.name)


@router.message(ClientForm.name)
async def get_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Введите имя")
        return

    await state.update_data(name=message.text)

    await message.answer("Сколько вам лет?")
    await state.set_state(ClientForm.age)


@router.message(ClientForm.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("Возраст должен быть числом (18–100)")
        return

    age = int(message.text)

    if age < 18 or age > 100:
        await message.answer("Возраст должен быть от 18 до 100")
        return

    await state.update_data(age=age)

    await message.answer("Ваш часовой пояс / страна?")
    await state.set_state(ClientForm.timezone)


@router.message(ClientForm.timezone)
async def get_timezone(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Введите страну или часовой пояс")
        return

    await state.update_data(timezone=message.text)

    await message.answer("Какой у вас запрос?")
    await state.set_state(ClientForm.request)


@router.message(ClientForm.request)
async def get_request(message: Message, state: FSMContext):
    if not message.text:
        return

    await state.update_data(request=message.text)

    await message.answer("Был ли опыт терапии?")
    await state.set_state(ClientForm.therapy)


@router.message(ClientForm.therapy)
async def get_therapy(message: Message, state: FSMContext):
    if not message.text:
        return

    await state.update_data(therapy_experience=message.text)

    await message.answer("Уровень тревоги (низкий / средний / высокий)?")
    await state.set_state(ClientForm.anxiety)


@router.message(ClientForm.anxiety)
async def get_anxiety(message: Message, state: FSMContext):
    if not message.text:
        return

    await state.update_data(anxiety_level=message.text)

    await message.answer("Удобный способ связи?")
    await state.set_state(ClientForm.contact)


@router.message(ClientForm.contact)
async def finish_form(message: Message, state: FSMContext):
    if not message.text:
        return

    await state.update_data(contact_method=message.text)

    data = await state.get_data()

    user = message.from_user
    if user is None:
        return

    client_data: ClientData = {
        "user_id": user.id,
        "name": data["name"],
        "age": data["age"],
        "timezone": data["timezone"],
        "request": data["request"],
        "therapy_experience": data["therapy_experience"],
        "anxiety_level": data["anxiety_level"],
        "contact_method": data["contact_method"],
    }

    save_client(client_data)

    await message.answer("Спасибо! Анкета сохранена ✅\nМы скоро с вами свяжемся.")

    await state.clear()
