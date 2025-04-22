from aiogram import BaseMiddleware

from bot.db.base import ExcelDB


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, database: ExcelDB) -> None:
        self.database = database

    async def __call__(self, handler, event, data):
        data["db"] = self.database
        return await handler(event, data)
