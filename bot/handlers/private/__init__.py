from aiogram import Router

from bot.middlewares import Middleware

from .admin import reg_handler as admin_handler
from .application import reg_handler as app_handler
from .help import reg_handler as help_handler
from .start import reg_handler as start_handler


def setup(bot) -> Router:
    router: Router = Router(name="privateChats")

    middleware = Middleware(bot, router)
    middleware.setup("db")
    middleware.setup("notify")
    middleware.setup("tour")

    start_handler(router)
    help_handler(router)
    app_handler(router)
    admin_handler(router)

    return router
