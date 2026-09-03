from datetime import date

from codescape.util.datetime import is_weekend


def test_is_weekend() -> None:
    assert is_weekend(date(2026, 9, 5)) is True  # Saturday
    assert is_weekend(date(2026, 9, 6)) is True  # Sunday
    assert is_weekend(date(2026, 9, 7)) is False  # Monday
    assert is_weekend(date(2026, 9, 8)) is False  # Tuesday
    assert is_weekend(date(2026, 9, 9)) is False  # Wednesday
    assert is_weekend(date(2026, 9, 10)) is False  # Thursday
    assert is_weekend(date(2026, 9, 11)) is False  # Friday
