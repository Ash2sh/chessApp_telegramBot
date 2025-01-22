import asyncio
import logging

from . import handlers
from .config import bot, dp, logger
from .utils import notify


async def on_startup() -> None:
    # Notify superusers
    await notify.superusers("bot is running")


async def on_shutdown() -> None:
    logger.warning("Shutting down..")
    await bot.session.close()
    await dp.storage.close()
    logger.warning("Bye!")


async def main() -> None:
    # Setup handlers
    handlers.setup()

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
