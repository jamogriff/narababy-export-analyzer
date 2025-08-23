import datetime
from zoneinfo import ZoneInfo


def create_date_from_narababy_event(date: str, timezone: str) -> datetime.datetime:
    datetime_format = "%Y-%m-%d %H:%M:%S"
    new_datetime = datetime.datetime.strptime(date, datetime_format)
    return new_datetime.replace(tzinfo=ZoneInfo(timezone))
