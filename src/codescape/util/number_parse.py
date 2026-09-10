from decimal import Decimal


def clean_float(value: str) -> float:
    """Removes thousands separators (commas) and converts to float."""
    if not value or value.strip() == "":
        return 0.0
    # Removes commas: "1,234.56" -> "1234.56"
    return float(value.replace(",", ""))


def clean_decimal(value: str) -> Decimal:
    """Removes thousands separators (commas) and converts to Decimal."""
    if not value or value.strip() == "":
        return Decimal("0.0")
    return Decimal(value.replace(",", ""))
