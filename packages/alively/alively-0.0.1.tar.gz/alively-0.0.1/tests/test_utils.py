import datetime as dt
from alively.utils import format_timedelta


def test_format_timedelta():
    assert format_timedelta(dt.timedelta(seconds=61)) == "01:01"
    assert format_timedelta(dt.timedelta(seconds=59)) == "00:59"
    assert format_timedelta(dt.timedelta(seconds=0)) == "00:00"
    assert format_timedelta(dt.timedelta(seconds=1)) == "00:01"
    assert format_timedelta(dt.timedelta(seconds=120)) == "02:00"
    assert format_timedelta(dt.timedelta(seconds=121)) == "02:01"
