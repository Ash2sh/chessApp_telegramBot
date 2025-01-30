from aiogram import BaseMiddleware
from sqlalchemy.orm import sessionmaker


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker: sessionmaker) -> None:
        self.sessionmaker = sessionmaker

    async def __call__(self, handler, event, data):
        data["db"] = self.sessionmaker()
        return await handler(event, data)
