from aiogram import Router

from .start import reg_handler as start_handler
from .application import reg_handler as app_handler

def setup() -> Router:
    router: Router = Router(name = "privateChats")

    start_handler(router)
    app_handler(router)

    return router