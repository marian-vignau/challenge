"""
Functions used to make some time calc.
"""
from datetime import time, datetime


def read_hour(hour_str: str, end_of_minute=False) -> time:
    """Convert a str in time."""
    hour = time.fromisoformat(hour_str)
    if hour.minute == 0 and hour.hour == 0:
        # in the rates table, 00:00 means the end of day
        # so, this is needed to avoid confusions.
        return time.max
    if end_of_minute:
        return time(
            hour=hour.hour,
            minute=hour.minute,
            second=time.max.second,
            microsecond=time.max.microsecond,
        )

    return hour


def diff_minutes(segment: dict) -> int:
    """Computes the difference in two different times

    Return the result in rounded minutes to avoid small differences."""
    time_point = lambda key: datetime.combine(datetime.now(), segment[key])
    delta = time_point("end") - time_point("start")
    return round(delta.seconds / 60)
