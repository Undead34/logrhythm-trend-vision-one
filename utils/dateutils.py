from datetime import datetime, timezone, timedelta


def parse_ISO_8601(data: str):
    try:
        date = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date.astimezone(timezone.utc)
    except:
        return None


def startDateTime(minutes=5):
    time = datetime.now(tz=timezone.utc) - timedelta(minutes=minutes)
    return time.isoformat(timespec="seconds").replace('+00:00', 'Z')


def endDateTime():
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds").replace('+00:00', 'Z')


def get_left_days(date: datetime):
    today = datetime.now(tz=timezone.utc)
    return (date - today).days
