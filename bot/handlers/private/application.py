import re

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.config import dp


class States(StatesGroup):
    firstSur_name = State()
    birthYear = State()
    sex = State()
    ageCategory = State()
    ratingFIDE = State()
    classRank = State()
    innPin = State()
    criteria = State()
    status = State()


LATIN_REGEX = re.compile(r"^[A-Za-z ]+$")


async def app_call_handler(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        "Привет! Пожалуйста, введите вашу Фамилию и Имя (только латинские буквы):"
    )
    await call.answer()

    await state.set_state(States.firstSur_name)


async def firstSur_name_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите ваш год рождения")

    await state.set_state(States.birthYear)


async def birthYear_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите ваш пол")

    await state.set_state(States.sex)


async def sex_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите вашу возрастную категорию")

    await state.set_state(States.ageCategory)


async def ageCategory_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите ваш рейтинг ФИДЕ")

    await state.set_state(States.ratingFIDE)


async def ratingFIDE_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите ваш разряд")

    await state.set_state(States.classRank)


async def class_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите ваш ИНН/ПИН")

    await state.set_state(States.innPin)


async def innPin_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите ваш критерий")

    await state.set_state(States.criteria)


async def сriteria_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите ваш статус")

    await state.set_state(States.status)


async def status_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите ваш год рождения")


def reg_handler() -> None:
    dp.callback_query.register(app_call_handler, F.data == "application")
    dp.message.register(
        firstSur_name_handler, F.text.strip().regexp(LATIN_REGEX), States.firstSur_name
    )
    dp.message.register(birthYear_handler, States.birthYear)
    dp.message.register(sex_handler, States.sex)
    dp.message.register(ageCategory_handler, States.ageCategory)
    dp.message.register(ratingFIDE_handler, States.ratingFIDE)
    dp.message.register(class_handler, States.classRank)
    dp.message.register(innPin_handler, States.innPin)
    dp.message.register(сriteria_handler, States.criteria)
    dp.message.register(status_handler, States.status)
