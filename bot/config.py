import logging
from os import getenv

from aiogram import Bot, Dispatcher

logger: logging.Logger = logging.getLogger()

dp: Dispatcher = Dispatcher()
bot: Bot = Bot(token=getenv("TOKEN"))

superUsers: list[int] = list(map(int, getenv("SUPER_USERS").split(' ')))