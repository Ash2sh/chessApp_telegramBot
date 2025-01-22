from aiogram import Bot

class Broadcaster:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_text(self, chats: list[int], message: str, parse_mode: str | None = None) -> None:
        for chat_id in chats:
            await self.bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode)