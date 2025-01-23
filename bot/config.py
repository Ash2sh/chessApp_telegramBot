import logging
from os import getenv

from aiogram import Bot, Dispatcher
from sqlalchemy import URL

logger: logging.Logger = logging.getLogger()

dp: Dispatcher = Dispatcher()
bot: Bot = Bot(token=getenv("TOKEN"))

superUsers: list[int] = [int(i) for i in getenv("SUPER_USERS").split(" ")]

dbUrl = getenv("DATABASE_URL", None)
# if not dbUrl:
#     dbUsername = getenv("DB_USERNAME", "")
#     dbPassword = getenv("DB_PASSWORD", "")
#     DB = {
#         "drivername": getenv("DB_DRIVER"),
#         "username": dbUsername if dbUsername else None,
#         "password": dbPassword if dbPassword else None,
#         "host": getenv("DB_HOST"),
#         "port": getenv("DB_PORT"),
#         "database": getenv("DB_DATABASE"),
#     }
#     dbUrl = URL.create(**DB)

# print(dbUrl)