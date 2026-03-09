"""Unit tests for mpg_to_kml.cli.main module."""

import pytest
from unittest.mock import patch, call
from io import StringIO

from mpg_to_kml.cli.main import get_float_input, main


# ---------------------------------------------------------------------------
# get_float_input — normal values
# ---------------------------------------------------------------------------


class TestGetFloatInputNormalValues:
    """Tests for valid positive numeric input."""

    @patch("builtins.input", return_value="30")
    def test_returns_float_for_integer_string(self, mock_input):
        """Integer string '30' should be returned as float 30.0."""
        result = get_float_input("Enter MPG: ")
        assert result == 30.0
        assert isinstance(result, float)

    @patch("builtins.input", return_value="28.5")
    def test_returns_float_for_decimal_string(self, mock_input):
        """Decimal string '28.5' should be returned as float 28.5."""
        result = get_float_input("Enter MPG: ")
        assert result == 28.5

    @patch("builtins.input", return_value="1")
    def test_minimum_valid_value(self, mock_input):
        """Value of 1 is the minimum meaningful positive input."""
        result = get_float_input("Prompt: ")
        assert result == 1.0

    @patch("builtins.input", return_value="1000000")
    def test_large_value(self, mock_input):
        """Very large numeric string should parse without error."""
        result = get_float_input("Prompt: ")
        assert result == 1_000_000.0

    @patch("builtins.input", return_value="0.001")
    def test_small_positive_value(self, mock_input):
        """Very small positive string (0.001) should be accepted."""
        result = get_float_input("Prompt: ")
        assert result == pytest.approx(0.001)

    @patch("builtins.input", return_value="42")
    def test_passes_prompt_to_input(self, mock_input):
        """Prompt text must be forwarded to the input() call."""
        get_float_input("Enter value: ")
        mock_input.assert_called_once_with("Enter value: ")


# ---------------------------------------------------------------------------
# get_float_input — edge cases (retry loop)
# ---------------------------------------------------------------------------


class TestGetFloatInputEdgeCases:
    """Tests for the retry loop triggered by invalid inputs."""

    @patch("builtins.input", side_effect=["0", "10"])
    def test_zero_retries_then_accepts_positive(self, mock_input, capsys):
        """Zero input must be rejected; subsequent positive value accepted."""
        result = get_float_input("Prompt: ")
        assert result == 10.0
        captured = capsys.readouterr()
        assert "0" in captured.out or len(captured.out) > 0

    @patch("builtins.input", side_effect=["-5", "25"])
    def test_negative_retries_then_accepts_positive(self, mock_input, capsys):
        """Negative input must be rejected; subsequent positive value accepted."""
        result = get_float_input("Prompt: ")
        assert result == 25.0

    @patch("builtins.input", side_effect=["abc", "30"])
    def test_non_numeric_string_retries(self, mock_input, capsys):
        """Non-numeric string must prompt a retry, then accept valid input."""
        result = get_float_input("Prompt: ")
        assert result == 30.0
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    @patch("builtins.input", side_effect=["", "15"])
    def test_empty_string_retries(self, mock_input, capsys):
        """Empty string must cause a retry."""
        result = get_float_input("Prompt: ")
        assert result == 15.0

    @patch("builtins.input", side_effect=["abc", "-1", "0", "20"])
    def test_multiple_invalid_inputs_before_valid(self, mock_input, capsys):
        """Multiple consecutive invalid inputs must all be rejected before accepting."""
        result = get_float_input("Prompt: ")
        assert result == 20.0
        assert mock_input.call_count == 4

    @patch("builtins.input", side_effect=["  ", "5"])
    def test_whitespace_string_retries(self, mock_input, capsys):
        """Whitespace-only string must cause a retry."""
        result = get_float_input("Prompt: ")
        assert result == 5.0


# ---------------------------------------------------------------------------
# get_float_input — unexpected input types (simulated)
# ---------------------------------------------------------------------------


class TestGetFloatInputUnexpectedErrors:
    """Tests for edge-case inputs that exercise error handling."""

    @patch("builtins.input", side_effect=["None", "10"])
    def test_none_string_retries(self, mock_input, capsys):
        """The literal string 'None' is not a valid number — must retry."""
        result = get_float_input("Prompt: ")
        assert result == 10.0

    @patch("builtins.input", side_effect=["inf", "10"])
    def test_inf_string_behaviour(self, mock_input, capsys):
        """'inf' parses as float('inf') which is > 0, so it may be accepted."""
        # float("inf") > 0 is True, so the implementation accepts it.
        result = get_float_input("Prompt: ")
        # Result is either inf (accepted) or 10 (if implementation rejects inf)
        assert result > 0

    @patch("builtins.input", side_effect=["nan", "10"])
    def test_nan_string_behaviour(self, mock_input, capsys):
        """'nan' parses as float('nan'); nan > 0 is False so it must retry."""
        result = get_float_input("Prompt: ")
        assert result == 10.0


# ---------------------------------------------------------------------------
# main() — integration tests with mocked I/O
# ---------------------------------------------------------------------------


class TestMainNormalValues:
    """Tests for main() with valid inputs and a working price scraper."""

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=750.0)
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_runs_without_exception(self, mock_input, mock_price):
        """main() must complete without raising for valid inputs."""
        main()  # should not raise

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=750.0)
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_prints_efficiency(self, mock_input, mock_price, capsys):
        """Output must contain the km/l efficiency value."""
        main()
        captured = capsys.readouterr()
        assert "km/l" in captured.out

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=750.0)
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_prints_distance(self, mock_input, mock_price, capsys):
        """Output must echo the distance traveled."""
        main()
        captured = capsys.readouterr()
        assert "100" in captured.out

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=750.0)
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_prints_total_cost(self, mock_input, mock_price, capsys):
        """Output must include a monetary cost figure."""
        main()
        captured = capsys.readouterr()
        assert "₡" in captured.out

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=750.0)
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_prints_price_per_liter(self, mock_input, mock_price, capsys):
        """Output must display the price per liter used."""
        main()
        captured = capsys.readouterr()
        assert "750" in captured.out

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=697.0)
    @patch("builtins.input", side_effect=["25", "200"])
    def test_main_uses_price_from_recope(self, mock_input, mock_price, capsys):
        """main() must use the price returned by get_recope_super_price()."""
        main()
        mock_price.assert_called_once()
        captured = capsys.readouterr()
        assert "697" in captured.out


# ---------------------------------------------------------------------------
# main() — edge cases
# ---------------------------------------------------------------------------


class TestMainEdgeCases:
    """Tests for main() boundary conditions."""

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=750.0)
    @patch("builtins.input", side_effect=["0", "30", "100"])
    def test_main_retries_on_zero_mpg(self, mock_input, mock_price, capsys):
        """main() must keep prompting until a positive MPG is entered."""
        main()
        captured = capsys.readouterr()
        assert "30" in captured.out

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=750.0)
    @patch("builtins.input", side_effect=["30", "0", "100"])
    def test_main_retries_on_zero_kms(self, mock_input, mock_price, capsys):
        """main() must keep prompting until a positive distance is entered."""
        main()
        captured = capsys.readouterr()
        assert "100" in captured.out

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=750.0)
    @patch("builtins.input", side_effect=["bad", "30", "100"])
    def test_main_retries_on_non_numeric_mpg(self, mock_input, mock_price, capsys):
        """main() must keep prompting when a non-numeric MPG is entered."""
        main()  # should not raise

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=750.0)
    @patch("builtins.input", side_effect=["50.5", "300.75"])
    def test_main_accepts_float_inputs(self, mock_input, mock_price, capsys):
        """main() must correctly handle floating-point user inputs."""
        main()
        captured = capsys.readouterr()
        assert "50.5" in captured.out


# ---------------------------------------------------------------------------
# main() — unexpected / error scenarios
# ---------------------------------------------------------------------------


class TestMainUnexpectedErrors:
    """Tests for main() behaviour under error conditions."""

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=0)
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_raises_on_zero_price(self, mock_input, mock_price):
        """main() must raise ValueError when the scraper returns 0."""
        with pytest.raises(ValueError, match="Invalid price"):
            main()

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=-100.0)
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_raises_on_negative_price(self, mock_input, mock_price):
        """main() must raise ValueError when the scraper returns a negative price."""
        with pytest.raises(ValueError, match="Invalid price"):
            main()

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=None)
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_raises_on_none_price(self, mock_input, mock_price):
        """main() must raise ValueError when the scraper returns None."""
        with pytest.raises(ValueError, match="Invalid price"):
            main()

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value=True)
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_raises_on_bool_price(self, mock_input, mock_price):
        """main() must raise ValueError when the scraper returns a boolean."""
        with pytest.raises(ValueError, match="Invalid price"):
            main()

    @patch("mpg_to_kml.cli.main.get_recope_super_price", return_value="750")
    @patch("builtins.input", side_effect=["30", "100"])
    def test_main_raises_on_string_price(self, mock_input, mock_price):
        """main() must raise ValueError when the scraper returns a string."""
        with pytest.raises(ValueError, match="Invalid price"):
            main()
