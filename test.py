import pytz
from datetime import datetime, date, time

timezone = pytz.timezone("Asia/Bishkek")
targetTime = time(3, 54, tzinfo=timezone)
dateNow = date.today()
print(datetime.now() < datetime.combine(dateNow, targetTime, timezone))