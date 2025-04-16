from aiogram import Bot, Dispatcher, Router

from bot.config import logger

from . import private


def setup(dp: Dispatcher, bot: Bot) -> None:
    logger.debug("Handlers start to initialize")

    privateChats: Router = private.setup(bot)

    dp.include_routers(privateChats)

    logger.info("Handlers initialized")
