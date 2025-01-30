import re
from datetime import date

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.orm import Session

from bot import db as DB
from bot.config import logger
from bot.utils.keyboard import InlineKeyboard, InlineKeyboardMarkup


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
    userId: int = call.from_user.id
    await state.set_data({"id": int})

    await call.message.edit_text(
        "Привет! Пожалуйста, введите вашу Фамилию и Имя (только латинские буквы):"
    )
    await call.answer()

    await state.set_state(States.firstSur_name)


async def firstSur_name_handler(message: Message, state: FSMContext) -> None:
    name: str = message.text.strip()
    if LATIN_REGEX.match(name):
        await state.set_data({"firstSurName": name})

        await message.answer("Введите ваш год рождения")

        await state.set_state(States.birthYear)
    else:
        await message.answer("Текст должен содержать только латинские буквы")


async def birthYear_handler(message: Message, state: FSMContext) -> None:
    text = message.text.strip()
    if text.isnumeric():
        year: int = int(text)
        currentYear: int = date.today().year
        age: int = currentYear - year
        if 0 < age < 150:
            buttons: list[dict] = [
                {"text": "Мужчина", "callback_data": "male"},
                {"text": "Женщина", "callback_data": "female"},
            ]
            markup: InlineKeyboardMarkup = InlineKeyboard(buttons).markup()

            await message.answer("Введите ваш пол", reply_markup=markup)
            await state.set_data({"birthYear": year})

            await state.set_state(States.sex)

            return

    await message.answer("Введите достоверный год рождения")


async def sex_handler(call: CallbackQuery, state: FSMContext) -> None:
    buttons = [
        {"text": "Open U6", "callback_data": "open_u6"},
        {"text": "Girls U6", "callback_data": "girls_u6"},
        {"text": "Open U8", "callback_data": "open_u8"},
        {"text": "Girls U8", "callback_data": "girls_u8"},
        {"text": "Open U10", "callback_data": "open_u10"},
        {"text": "Girls U10", "callback_data": "girls_u10"},
        {"text": "Open U12", "callback_data": "open_u12"},
        {"text": "Girls U12", "callback_data": "girls_u12"},
        {"text": "Open U14", "callback_data": "open_u14"},
        {"text": "Girls U14", "callback_data": "girls_u14"},
        {"text": "Open U16", "callback_data": "open_u16"},
        {"text": "Girls U16", "callback_data": "girls_u16"},
        {"text": "Open U18", "callback_data": "open_u18"},
        {"text": "Girls U18", "callback_data": "girls_u18"},
        {"text": "Open U20", "callback_data": "open_u20"},
        {"text": "Girls U20", "callback_data": "girls_u20"},
        {"text": "Open", "callback_data": "open"},
        {"text": "Women", "callback_data": "women"},
        {"text": "Seniors 50+", "callback_data": "seniors_50"},
        {"text": "Seniors 65+", "callback_data": "seniors_65"},
    ]

    callData: str = call.data
    if callData == "male":
        await state.set_data({"sex": "M"})
        buttons = [i for i in buttons if "Open" in i["text"] or "Seniors" in i["text"]]

    elif callData == "female":
        await state.set_data({"sex": "F"})

    markup: InlineKeyboardMarkup = InlineKeyboard(buttons).markup()

    await call.message.edit_text(
        "Введите вашу возрастную категорию", reply_markup=markup
    )
    await call.answer()

    await state.set_state(States.ageCategory)


async def ageCategory_handler(call: CallbackQuery, state: FSMContext) -> None:
    category: str = call.data
    await state.set_data({"ageCategory": category})

    await call.message.edit_text("Введите ваш рейтинг ФИДЕ")
    await call.answer()

    await state.set_state(States.ratingFIDE)


async def ratingFIDE_handler(message: Message, state: FSMContext) -> None:
    rating: int = int(message.text.strip())
    await state.set_data({"ratingFIDE": rating})

    buttons: list[dict] = [
        {"text": "I", "callback_data": "1"},
        {"text": "II", "callback_data": "2"},
        {"text": "III", "callback_data": "3"},
    ]
    markup: InlineKeyboardMarkup = InlineKeyboard(buttons).markup()
    await message.answer("Введите ваш разряд", reply_markup=markup)

    await state.set_state(States.classRank)


async def class_handler(call: CallbackQuery, state: FSMContext) -> None:
    classRank: int = int(call.data)
    await state.set_data({"classRank": classRank})

    await call.message.edit_text("Введите ваш ИНН/ПИН")
    await call.answer()

    await state.set_state(States.innPin)


async def innPin_handler(message: Message, state: FSMContext) -> None:
    innPin: str = message.text.strip()
    await state.set_data({"innPin": innPin})

    buttons: list[dict] = [
        {
            "text": "Призер Чемпионата Мира",
            "callback_data": "global_champion",
        },
        {
            "text": "Призер Чемпионата Азии",
            "callback_data": "asian_champion",
        },
        {
            "text": "Призер Чемпионата Западной/Центральной Азии",
            "callback_data": "west_central_asia_champion",
        },
        {
            "text": "Призер Чемпионата Кыргызской Республики",
            "callback_data": "kyrgyz_republic_champion",
        },
        {
            "text": "Призер Чемпионата г.Бишкек/г.Ош",
            "callback_data": "bishkek_osh_champion",
        },
        {
            "text": "Призер Областных Чемпионатов",
            "callback_data": "regional_champion",
        },
        {
            "text": "Квота шах-го Клуба/Школы",
            "callback_data": "quota_club_school",
        },
    ]
    markup: InlineKeyboardMarkup = InlineKeyboard(buttons).markup()

    await message.answer("Введите ваш критерий", reply_markup=markup)

    await state.set_state(States.criteria)


async def сriteria_handler(call: CallbackQuery, state: FSMContext) -> None:
    criteria: str = call.data
    await state.set_data({"criteria": criteria})

    buttons: list[dict] = [
        {"text": "Основной игрок", "callback_data": "main_player"},
        {"text": "Запасной игрок", "callback_data": "second_player"},
    ]
    markup: InlineKeyboardMarkup = InlineKeyboard(buttons).markup()

    await call.message.edit_text("Введите ваш статус", reply_markup=markup)
    await call.answer()

    await state.set_state(States.status)


async def status_handler(call: CallbackQuery, state: FSMContext, db: Session) -> None:
    status: str = call.data
    await state.set_data({"status": status})

    data: dict = await state.get_data()
    dbUser: DB.User = DB.User(**data)
    db.add(dbUser)
    await db.commit()

    await call.message.edit_text("Все готово")


def reg_handler(router: Router) -> None:
    router.callback_query.register(app_call_handler, F.data == "application")
    router.message.register(firstSur_name_handler, States.firstSur_name)
    router.message.register(birthYear_handler, States.birthYear)
    router.callback_query.register(sex_handler, States.sex)
    router.callback_query.register(ageCategory_handler, States.ageCategory)
    router.message.register(ratingFIDE_handler, F.text.isnumeric(), States.ratingFIDE)
    router.callback_query.register(class_handler, States.classRank)
    router.message.register(innPin_handler, States.innPin)
    router.callback_query.register(сriteria_handler, States.criteria)
    router.callback_query.register(status_handler, States.status)

    logger.debug("Application handler registered")
