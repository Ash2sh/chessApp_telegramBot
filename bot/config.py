import logging
from os import getenv

import pytz

logger: logging.Logger = logging.getLogger(name="bot")

logPath = "logs"
dataPath = "data"

TOKEN: str = getenv("TOKEN")  # Example: "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"


username = "TaSH1R000"
API_TOKEN = getenv("API_TOKEN")

timezone = pytz.timezone("Asia/Bishkek")

AUTO_CHAT_ID = 943922098
AUTO_TOPIC_ID = 2

superUsers: list[int] = [
    int(i) for i in getenv("SUPER_USERS").split(" ")
]  # Example: "123456789 ..."
