from bot.config import dp
from bot.db.base import create_pool

from .database import DatabaseMiddleware


def setup() -> None:
    db_middleware: DatabaseMiddleware = DatabaseMiddleware(create_pool())
    dp.message.middleware(db_middleware)
    dp.callback_query.middleware(db_middleware)