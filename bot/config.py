import logging
from os import getenv

logger: logging.Logger = logging.getLogger(name="bot")

TOKEN: str = getenv("TOKEN")  # Example: "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"

superUsers: list[int] = [
    int(i) for i in getenv("SUPER_USERS").split(" ")
]  # Example: "123456789 ..."

dbUrl: str = getenv(
    "DATABASE_URL"
)  # Example: "postgresql+asyncpg://name:password@host:port/dbname"
