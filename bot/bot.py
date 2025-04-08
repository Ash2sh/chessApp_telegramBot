import asyncio
import logging

from aiogram import Bot, Dispatcher

from . import handlers
from .config import TOKEN, logger
from .middlewares.broadcaster import Notify


async def on_startup(bot: Bot) -> None:
    logger.info("Bot is running")

    await Notify(bot).superusers("bot is running")


async def on_shutdown() -> None:
    logger.warning("Shutting down..")


async def main() -> None:
    dp: Dispatcher = Dispatcher()
    bot: Bot = Bot(token=TOKEN)

    handlers.setup(dp, bot)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


def cli():
    """Wrapper for command line"""
    try:
        logging.basicConfig(level=logging.DEBUG)
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
