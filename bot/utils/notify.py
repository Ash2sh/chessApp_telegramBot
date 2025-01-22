from bot.config import bot, superUsers
from .Broadcaster import Broadcaster

bc = Broadcaster(bot)

async def superusers(message: str) -> None:
    await bc.send_text(superUsers, message)
