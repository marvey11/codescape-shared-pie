from decimal import Decimal

from codescape.util.number_parse import clean_decimal, clean_float


class TestNumberParser:
    """Test class for number parsing utilities."""

    def test_clean_float(self) -> None:
        assert clean_float("") == 0.0
        assert clean_float("  ") == 0.0
        assert clean_float("0") == 0.0
        assert clean_float("0.0") == 0.0
        assert clean_float("1234.56") == 1234.56
        assert clean_float("1,234.56") == 1234.56

    def test_clean_decimal(self) -> None:
        assert clean_decimal("") == Decimal("0.0")
        assert clean_decimal("  ") == Decimal("0.0")
        assert clean_decimal("0") == Decimal("0.0")
        assert clean_decimal("0.0") == Decimal("0.0")
        assert clean_decimal("1234.56") == Decimal("1234.56")
        assert clean_decimal("1,234.56") == Decimal("1234.56")
