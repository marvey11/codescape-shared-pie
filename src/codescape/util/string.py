"""String module."""


def shorten_string(str_long: str, max_length: int, marker: str = "") -> str:
    """
    Shortens a string to a maximum length.

    A marker can be added to the end of the string (for example `...`).

    Args:
        str_long (str):
            the string that may need shortening.
        max_length (int):
            the maximum length the resulting can have when returned.
        marker (str):
            the optional marker that will be added at the end of the string, e.g. three
            dots `...`; the original string will be shortened to accomodate the marker
            so that the length of the returned string will not exceed the maximum value.

    Returns:
        The string that may or may not have been shortened. The length of the returned
        string may not exceed the maximum length specified by `max_length`.

    Raises:
        ValueError: if the maximum is negative.
    """
    if max_length < 0:
        raise ValueError("maximum length must be non-negative")

    return (
        str_long
        if len(str_long) <= max_length
        else (str_long[0 : (max_length - len(marker))] + marker)[0:max_length]
    )
