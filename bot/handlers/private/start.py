from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.config import logger


async def start(message: Message) -> None:
    keyboard: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text="Подать заявку", callback_data="application")]
    ]
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await message.answer(
        "Это тестовый бот для подачи заявок на шахматные турниры",
        reply_markup=markup,
    )


def reg_handler(router: Router) -> None:
    router.message.register(start, Command(commands=["start"]))

    logger.debug("Start handler registered")
