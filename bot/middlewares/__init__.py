from aiogram import Bot, Router, BaseMiddleware

from bot.config import logger
from bot.db.base import create_pool

from .broadcaster import NotifyMiddleware
from .database import DatabaseMiddleware


class Middleware:
    def __init__(self, bot: Bot, router: Router) -> None:
        self.router = router
        self.middlewares: dict[BaseMiddleware] = {
            "db": DatabaseMiddleware(create_pool()),
            "notify": NotifyMiddleware(bot),
        }

    def setup(self, middleware: str) -> None:
        logger.debug(f"Set {middleware} middleware, on {self.router.name} router")

        mw = self.middlewares.get(middleware, None)
        if mw is None:
            logger.error(f"Unknown middleware: {middleware}")
            return

        self.router.message.middleware(mw)
        self.router.callback_query.middleware(mw)
