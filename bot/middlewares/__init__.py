from aiogram import BaseMiddleware, Bot, Router

from bot.config import API_TOKEN, dataPath, logger
from bot.db.user import User

from .broadcaster import NotifyMiddleware
from .database import DatabaseMiddleware
from .tournament import TournamentMiddleware


class Middleware:
    def __init__(self, bot: Bot, router: Router) -> None:
        self.router = router
        self.middlewares: dict[BaseMiddleware] = {
            "db": DatabaseMiddleware(User(dataPath + "/users.xlsx")),
            "notify": NotifyMiddleware(bot),
            "tour": TournamentMiddleware(API_TOKEN),
        }

    def setup(self, middleware: str) -> None:
        logger.debug(f"Set {middleware} middleware, on {self.router.name} router")

        mw = self.middlewares.get(middleware, None)
        if mw is None:
            logger.error(f"Unknown middleware: {middleware}")
            return

        self.router.message.middleware(mw)
        self.router.callback_query.middleware(mw)
