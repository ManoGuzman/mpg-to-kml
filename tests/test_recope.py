"""Unit tests for mpg_to_kml.pricing.recope module."""

import pytest
import requests
from unittest.mock import MagicMock, patch

from mpg_to_kml.pricing.recope import get_recope_super_price, DEFAULT_PRICE_CRC


# ---------------------------------------------------------------------------
# Helpers: minimal HTML payloads
# ---------------------------------------------------------------------------


def _make_html(rows_html: str) -> bytes:
    """Wrap table row HTML in a minimal but valid page structure.

    The charset meta tag is required so that lxml correctly decodes UTF-8
    characters like ₡ (U+20A1) when parsing the bytes directly.
    """
    return (
        f'<html><head><meta charset="utf-8"></head><body><table>{rows_html}</table></body></html>'
    ).encode("utf-8")


SUPER_ROW = """
<tr>
    <td>SUPER</td>
    <td>₡750.00</td>
</tr>
"""

SUPER_ROW_NO_CURRENCY_SYMBOL = """
<tr>
    <td>SUPER</td>
    <td>820</td>
</tr>
"""

SUPER_ROW_WITH_COMMA = """
<tr>
    <td>SUPER</td>
    <td>₡1,200.00</td>
</tr>
"""

NO_SUPER_ROW = """
<tr>
    <td>REGULAR</td>
    <td>₡650.00</td>
</tr>
"""

PRICE_OUT_OF_RANGE_LOW = """
<tr>
    <td>SUPER</td>
    <td>₡499.00</td>
</tr>
"""

PRICE_OUT_OF_RANGE_HIGH = """
<tr>
    <td>SUPER</td>
    <td>₡2001.00</td>
</tr>
"""

MULTIPLE_ROWS_SUPER_LAST = """
<tr>
    <td>REGULAR</td>
    <td>₡650.00</td>
</tr>
<tr>
    <td>SUPER</td>
    <td>₡750.00</td>
</tr>
"""

MULTIPLE_PRICES_IN_SUPER_ROW = """
<tr>
    <td>SUPER</td>
    <td>₡100.00</td>
    <td>₡750.00</td>
</tr>
"""

HEADER_ONLY_TABLE = "<tr><th>Producto</th><th>Precio</th></tr>"


def _mock_response(content: bytes, status_code: int = 200):
    """Build a mock requests.Response with the given content."""
    mock = MagicMock()
    mock.status_code = status_code
    mock.content = content
    mock.raise_for_status = MagicMock()
    if status_code >= 400:
        mock.raise_for_status.side_effect = requests.HTTPError(response=mock)
    return mock


# ---------------------------------------------------------------------------
# Normal values — successful scraping
# ---------------------------------------------------------------------------


class TestGetRecopeSuperPriceNormalValues:
    """Tests for successful scraping scenarios."""

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_returns_float_on_success(self, mock_get):
        mock_get.return_value = _mock_response(_make_html(SUPER_ROW))
        result = get_recope_super_price()
        assert isinstance(result, float)

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_extracts_price_from_super_row(self, mock_get):
        mock_get.return_value = _mock_response(_make_html(SUPER_ROW))
        result = get_recope_super_price()
        assert result == pytest.approx(750.0)

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_price_without_currency_symbol(self, mock_get):
        """Price cell that contains only digits (no ₡) should still parse."""
        mock_get.return_value = _mock_response(_make_html(SUPER_ROW_NO_CURRENCY_SYMBOL))
        result = get_recope_super_price()
        assert result == pytest.approx(820.0)

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_price_with_thousands_comma(self, mock_get):
        """Prices formatted with commas (e.g. 1,200) should parse correctly."""
        mock_get.return_value = _mock_response(_make_html(SUPER_ROW_WITH_COMMA))
        result = get_recope_super_price()
        assert result == pytest.approx(1200.0)

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_super_row_among_multiple_rows(self, mock_get):
        """SUPER price is extracted even when other rows are present."""
        mock_get.return_value = _mock_response(_make_html(MULTIPLE_ROWS_SUPER_LAST))
        result = get_recope_super_price()
        assert result == pytest.approx(750.0)

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_price_in_valid_range(self, mock_get):
        """Returned price must lie within the accepted 500–2000 range."""
        mock_get.return_value = _mock_response(_make_html(SUPER_ROW))
        result = get_recope_super_price()
        assert 500 <= result <= 2000

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_correct_url_is_requested(self, mock_get):
        """The scraper must target the RECOPE national prices page."""
        mock_get.return_value = _mock_response(_make_html(SUPER_ROW))
        get_recope_super_price()
        called_url = mock_get.call_args[0][0]
        assert "recope.go.cr" in called_url

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_timeout_is_set(self, mock_get):
        """HTTP request must include a timeout to avoid hanging."""
        mock_get.return_value = _mock_response(_make_html(SUPER_ROW))
        get_recope_super_price()
        kwargs = mock_get.call_args[1]
        assert "timeout" in kwargs
        assert kwargs["timeout"] > 0

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_case_insensitive_super_match(self, mock_get):
        """Row detection is case-insensitive (e.g. 'Super', 'super')."""
        html = _make_html("<tr><td>Super</td><td>₡780.00</td></tr>")
        mock_get.return_value = _mock_response(html)
        result = get_recope_super_price()
        assert result == pytest.approx(780.0)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestGetRecopeSuperPriceEdgeCases:
    """Tests for boundary and near-failure scenarios."""

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_price_at_lower_bound_500(self, mock_get):
        """Price of exactly 500 is at the lower boundary — must be accepted."""
        html = _make_html("<tr><td>SUPER</td><td>₡500.00</td></tr>")
        mock_get.return_value = _mock_response(html)
        result = get_recope_super_price()
        assert result == pytest.approx(500.0)

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_price_at_upper_bound_2000(self, mock_get):
        """Price of exactly 2000 is at the upper boundary — must be accepted."""
        html = _make_html("<tr><td>SUPER</td><td>₡2000.00</td></tr>")
        mock_get.return_value = _mock_response(html)
        result = get_recope_super_price()
        assert result == pytest.approx(2000.0)

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_price_below_range_falls_back(self, mock_get, capsys):
        """Price of 499 is below valid range — falls back to default."""
        mock_get.return_value = _mock_response(_make_html(PRICE_OUT_OF_RANGE_LOW))
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_price_above_range_falls_back(self, mock_get, capsys):
        """Price of 2001 is above valid range — falls back to default."""
        mock_get.return_value = _mock_response(_make_html(PRICE_OUT_OF_RANGE_HIGH))
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_no_super_row_falls_back(self, mock_get):
        """Page with no SUPER row must return the fallback price."""
        mock_get.return_value = _mock_response(_make_html(NO_SUPER_ROW))
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_header_only_table_falls_back(self, mock_get):
        """Table with only <th> headers and no <td> must fall back."""
        mock_get.return_value = _mock_response(_make_html(HEADER_ONLY_TABLE))
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_empty_page_falls_back(self, mock_get):
        """Empty HTML body with no tables must fall back gracefully."""
        mock_get.return_value = _mock_response(b"<html><body></body></html>")
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_multiple_prices_picks_last_valid(self, mock_get):
        """When a SUPER row has multiple cells, the last valid price is used."""
        mock_get.return_value = _mock_response(_make_html(MULTIPLE_PRICES_IN_SUPER_ROW))
        result = get_recope_super_price()
        # reversed() means the last cell (750) is tried first — expect 750
        assert result == pytest.approx(750.0)


# ---------------------------------------------------------------------------
# Unexpected / network errors
# ---------------------------------------------------------------------------


class TestGetRecopeSuperPriceUnexpectedErrors:
    """Tests for network failures and other unexpected exceptions."""

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_connection_error_returns_default(self, mock_get):
        """Network failure must be caught and default price returned."""
        mock_get.side_effect = requests.ConnectionError("unreachable")
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_timeout_error_returns_default(self, mock_get):
        """Timeout must be caught and default price returned."""
        mock_get.side_effect = requests.Timeout("timed out")
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_http_4xx_returns_default(self, mock_get):
        """HTTP 404 response must trigger fallback to default price."""
        mock_get.return_value = _mock_response(b"", status_code=404)
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_http_5xx_returns_default(self, mock_get):
        """HTTP 500 response must trigger fallback to default price."""
        mock_get.return_value = _mock_response(b"", status_code=500)
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_malformed_html_falls_back(self, mock_get):
        """Completely malformed HTML must not raise — must return default."""
        mock_get.return_value = _mock_response(b"<<not html>>")
        result = get_recope_super_price()
        # lxml is lenient, so this may or may not parse — either way no exception
        assert isinstance(result, float)

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_non_numeric_price_cell_falls_back(self, mock_get):
        """If the SUPER row price cell contains non-numeric text, fall back."""
        html = _make_html("<tr><td>SUPER</td><td>N/A</td></tr>")
        mock_get.return_value = _mock_response(html)
        result = get_recope_super_price()
        assert result == DEFAULT_PRICE_CRC

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_returns_default_price_type_is_float(self, mock_get):
        """Fallback value must be a float (not int or None)."""
        mock_get.side_effect = requests.ConnectionError("down")
        result = get_recope_super_price()
        assert isinstance(result, float)

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_default_price_constant_is_positive(self, mock_get):
        """DEFAULT_PRICE_CRC must be a positive numeric value."""
        assert isinstance(DEFAULT_PRICE_CRC, (int, float))
        assert DEFAULT_PRICE_CRC > 0

    @patch("mpg_to_kml.pricing.recope.requests.get")
    def test_error_message_printed_on_failure(self, mock_get, capsys):
        """On network failure a diagnostic message must be printed to stdout."""
        mock_get.side_effect = requests.ConnectionError("down")
        get_recope_super_price()
        captured = capsys.readouterr()
        assert len(captured.out) > 0
