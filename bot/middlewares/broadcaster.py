from aiogram import Bot, BaseMiddleware

from bot.config import superUsers


class NotifyMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def __call__(self, handler, event, data):
        data["notify"] = Notify(self.bot)
        return await handler(event, data)


class Broadcaster:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_text(
        self,
        chats: list[int],
        message: str,
        parse_mode: str | None = None,
    ) -> None:
        for chat_id in chats:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=parse_mode,
            )


class Notify(Broadcaster):
    async def superusers(self, message: str) -> None:
        await self.send_text(superUsers, message)
