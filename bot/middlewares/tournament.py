from aiogram import BaseMiddleware

from bot.utils.tournament import TournamentFactory


class TournamentMiddleware(BaseMiddleware):
    def __init__(self, api: str) -> None:
        self.api = api
        self.factory = TournamentFactory(self.api)

    async def __call__(self, handler, event, data):
        data["tour"] = self.factory
        return await handler(event, data)
