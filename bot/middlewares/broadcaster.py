from datetime import datetime

from aiogram import BaseMiddleware, Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from bot.config import AUTO_CHAT_ID, logger, superUsers, timezone
from bot.utils.tournament import Tournament


class NotifyMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def __call__(self, handler, event, data):
        data["notify"] = Notify(self.bot)
        return await handler(event, data)


class Broadcaster:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

    async def send_text(self, chats: list[int], message: str, **kwargs) -> None:
        for chat_id in chats:
            await self.bot.send_message(chat_id=chat_id, text=message, **kwargs)

    async def schedule_message(self, date: datetime, id: str, **kwargs) -> None:
        trigger = DateTrigger(date, timezone)
        self.scheduler.add_job(self.send_text, trigger=trigger, id=id, kwargs=kwargs)

    async def remove_schedule(self, id: str) -> None:
        job = self.scheduler.get_job(id)
        if job:
            self.scheduler.remove_job(id)
            logger.info(f"Сообщение {id} Успешно удалено")
        else:
            logger.error(f"Сообщение {id} не найдено")


class Notify(Broadcaster):
    async def superusers(self, message: str, **kwargs) -> None:
        await self.send_text(superUsers, message, **kwargs)

    async def tournament(self, tournament: Tournament) -> None:
        result: str = tournament.message()
        date: datetime = tournament.when()
        if "https://lichess.org/tournament/" in result:
            try:
                await self.schedule_message(
                    date,
                    tournament.get_id(),
                    chats=AUTO_CHAT_ID,
                    message=result,
                    parse_mode="HTML",
                )
                logger.info(f"✅ Турнир отправлен в {date.strftime("%Y-%m-%dT%H:%M:%S.%f")}")
            except Exception as e:
                logger.error(f"❌ Ошибка отправки: {e}")
        else:
            logger.error(f"❌ Ошибка создания турнира: {result}")
