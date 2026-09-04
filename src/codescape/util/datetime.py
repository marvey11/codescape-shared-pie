"""date and time utilities module"""

from datetime import date


def is_weekend(day: date) -> bool:
    """
    Checks whether the specified day is a weekend day (Saturday or Sunday).

    Args:
        day (date):
            the day to check.

    Returns:
        `True` if the specified day is a Saturday or Sunday, else `False`.
    """

    return day.isoweekday() > 5
