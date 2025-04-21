import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import date, datetime, time, timedelta

from . import handlers
from .config import TOKEN, logger, API_TOKEN, timezone, AUTO_CHAT_ID
from .middlewares.broadcaster import Notify
from .utils.tournament import TournamentParams, Tournament

TOURNAMENT_PARAMS = TournamentParams(
    name="Kyrgyzstan Arena",
    clockTime=3,
    clockIncrement=0,
    minutes=70,
    waitMinutes=5,
    variant="standard",
    rated=True,
    berserkable=True,
    streakable=True,
    description="Ежедневный онлайн турнир по блицу для всех желающих",
)

async def schedule_tournament(bot: Bot):
    tour = await Tournament.create(API_TOKEN, TOURNAMENT_PARAMS)
    await bot.send_message(AUTO_CHAT_ID, tour.message())


async def on_startup(bot: Bot) -> None:
    logger.info("Bot is running")

    await Notify(bot).superusers("bot is running")

    # lastDate: date | None = None
    # targetTime = time(3, 43)
    # sched = AsyncIOScheduler()
    # sched.start()
    # while True:
    #     dateNow = date.today()
    #     if lastDate != dateNow:
    #         lastDate = dateNow
    #         trigger = DateTrigger(datetime.combine(lastDate, targetTime, timezone))
    #         print(trigger)
    #         sched.add_job(schedule_tournament, trigger, args=[bot])
    #     await asyncio.sleep(18000)

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
