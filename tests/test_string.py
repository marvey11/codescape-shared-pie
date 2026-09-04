"""Tests for the utilities module."""

import pytest

from codescape.util.string import shorten_string


class TestStringUtilties:
    """Test class for all string utilities."""

    def test_shorten_string_empty_no_marker(self) -> None:
        """
        Tests whether an empty string (that consequently is shorter than the maximum
        length) is treated correctly.

        The marker is not used in this test.
        """
        original = ""
        result = shorten_string(original, 10)

        assert original == result

    def test_shorten_string_shorter_than_max_length_no_marker(self) -> None:
        """
        Tests whether a string that is shorter than the maximum length is treated
        correctly.

        The marker is not used in this test.
        """
        original = "test"
        result = shorten_string(original, 10)

        assert original == result

    def test_shorten_string_max_length_exactly_no_marker(self) -> None:
        """
        Tests whether a string that is exactly as long as the maximum length is treated
        correctly.

        The marker is not used in this test.
        """
        original = "testtesttest"
        result = shorten_string(original, 12)

        assert original == result

    def test_shorten_string_longer_than_max_length_no_marker(self) -> None:
        """
        Tests whether a string that is longer than the maximum length is treated
        correctly.

        The marker is not used in this test.
        """
        original = "testtesttesttest"
        result = shorten_string(original, 10)

        assert len(result) == 10
        assert original.startswith(result)

    def test_shorten_string_max_length_zero_no_marker(self) -> None:
        """
        Tests for a boundary case: maximum length is 0 --> should return an empty
        string.

        The marker is not used in this test.
        """
        original = "test"
        result = shorten_string(original, 0)

        assert result == ""

    def test_shorten_string_empty_with_marker(self) -> None:
        """
        Tests whether an empty string (that consequently is shorter than the maximum
        length) is treated correctly.

        The marker is used in this test. There should be no sign of the marker in the
        result.
        """
        original = ""
        result = shorten_string(original, 10, "...")

        assert original == result

    def test_shorten_string_shorter_than_max_length(self) -> None:
        """
        Tests whether a string that is shorter than the maximum length is treated
        correctly.

        The marker is used in this test. There should be no sign of the marker in the
        result.
        """
        original = "test"
        result = shorten_string(original, 10, "...")

        assert original == result

    def test_shorten_string_max_length_exactly_with_marker(self) -> None:
        """
        Tests whether a string that is exactly as long as the maximum length is treated
        correctly.

        The marker is used in this test. There should be no sign of the marker in the
        result.
        """
        original = "testtesttest"
        result = shorten_string(original, 12, "...")

        assert original == result

    def test_shorten_string_longer_than_max_length_with_marker(self) -> None:
        """
        Tests whether a string that is longer than the maximum length is treated
        correctly.

        The marker is used in this test.
        """
        original = "testtesttesttest"
        result = shorten_string(original, 10, "...")

        assert len(result) == 10
        assert result.endswith("...")
        assert original.startswith(result[0:7])

    def test_shorten_string_max_length_zero_with_marker(self) -> None:
        """
        Tests for a boundary case: the marker is used, but the maximum length is 0
        --> should still return an empty string.
        """
        original = "test"
        result = shorten_string(original, 0, "....")

        assert result == ""

    def test_shorten_string_max_length_negative(self) -> None:
        """Tests for an error case: The maximum length is negative."""

        with pytest.raises(ValueError, match="maximum length must be non-negative"):
            shorten_string("test", -1)
