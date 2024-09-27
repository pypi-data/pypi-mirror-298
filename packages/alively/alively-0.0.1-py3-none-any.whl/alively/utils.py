import datetime as dt


def format_timedelta(delta: dt.timedelta) -> str:
    minutes = delta.seconds // 60
    seconds = round(delta.seconds - 60 * minutes)
    return f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
