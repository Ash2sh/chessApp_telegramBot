from aiogram import Router, Dispatcher, Bot

from bot.middlewares import Middleware
from bot.config import logger
from . import private


def setup(dp: Dispatcher, bot: Bot) -> None:
    logger.debug("Handlers start to initialize")

    privateChats: Router = private.setup()
    Middleware(bot, privateChats).setup("db")

    dp.include_routers(privateChats)

    logger.info("Handlers initialized")