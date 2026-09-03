"""date and time utilities module"""

from datetime import date


def is_weekend(day: date) -> bool:
    """Returns True if the specified day is a Saturday or Sunday, else False."""

    return day.isoweekday() > 5
