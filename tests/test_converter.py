"""Unit tests for mpg_to_kml.conversion.converter module."""

import pytest
from mpg_to_kml.conversion.converter import mpg_to_kml, MPG_TO_KML_FACTOR


class TestMpgToKmlNormalValues:
    """Tests for expected, typical inputs."""

    def test_typical_city_mpg(self):
        """25 MPG is a common city fuel efficiency value."""
        result = mpg_to_kml(25)
        assert result == pytest.approx(25 * MPG_TO_KML_FACTOR)

    def test_typical_highway_mpg(self):
        """35 MPG is a common highway fuel efficiency value."""
        result = mpg_to_kml(35)
        assert result == pytest.approx(35 * MPG_TO_KML_FACTOR)

    def test_float_input(self):
        """Accepts float values and converts correctly."""
        result = mpg_to_kml(30.5)
        assert result == pytest.approx(30.5 * MPG_TO_KML_FACTOR)

    def test_integer_input(self):
        """Accepts integer values and converts correctly."""
        result = mpg_to_kml(20)
        assert result == pytest.approx(20 * MPG_TO_KML_FACTOR)

    def test_known_conversion(self):
        """1 MPG should equal exactly MPG_TO_KML_FACTOR km/l."""
        result = mpg_to_kml(1)
        assert result == pytest.approx(MPG_TO_KML_FACTOR)

    def test_high_efficiency_vehicle(self):
        """Hybrid/electric-equivalent vehicles can have very high MPG."""
        result = mpg_to_kml(50)
        assert result == pytest.approx(50 * MPG_TO_KML_FACTOR)

    def test_result_is_float(self):
        """Return value is always a float."""
        result = mpg_to_kml(10)
        assert isinstance(result, float)

    def test_large_mpg_value(self):
        """Large numeric values should convert without overflow."""
        result = mpg_to_kml(1000)
        assert result == pytest.approx(1000 * MPG_TO_KML_FACTOR)


class TestMpgToKmlEdgeCases:
    """Tests for boundary and edge-case inputs."""

    def test_very_small_positive_float(self):
        """Smallest representable positive float should still convert."""
        result = mpg_to_kml(1e-10)
        assert result == pytest.approx(1e-10 * MPG_TO_KML_FACTOR)

    def test_exactly_one_mpg(self):
        """Boundary value of 1 MPG (low-efficiency vehicle)."""
        result = mpg_to_kml(1.0)
        assert result == pytest.approx(MPG_TO_KML_FACTOR)

    def test_large_float_mpg(self):
        """Very large float value should not raise."""
        result = mpg_to_kml(1e9)
        assert result == pytest.approx(1e9 * MPG_TO_KML_FACTOR)

    def test_zero_raises_value_error(self):
        """Zero MPG is physically meaningless — must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            mpg_to_kml(0)

    def test_zero_float_raises_value_error(self):
        """0.0 (float zero) must also raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            mpg_to_kml(0.0)

    def test_negative_integer_raises_value_error(self):
        """Negative MPG has no physical meaning — must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            mpg_to_kml(-1)

    def test_negative_float_raises_value_error(self):
        """Negative float MPG must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            mpg_to_kml(-0.001)

    def test_very_large_negative_raises_value_error(self):
        """Large negative values must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            mpg_to_kml(-1e9)


class TestMpgToKmlUnexpectedErrors:
    """Tests for invalid / unexpected input types."""

    def test_string_raises_type_error(self):
        """String input must raise TypeError."""
        with pytest.raises(TypeError, match="numeric type"):
            mpg_to_kml("30")

    def test_none_raises_type_error(self):
        """None input must raise TypeError."""
        with pytest.raises(TypeError, match="numeric type"):
            mpg_to_kml(None)

    def test_list_raises_type_error(self):
        """List input must raise TypeError."""
        with pytest.raises(TypeError, match="numeric type"):
            mpg_to_kml([30])

    def test_dict_raises_type_error(self):
        """Dict input must raise TypeError."""
        with pytest.raises(TypeError, match="numeric type"):
            mpg_to_kml({"mpg": 30})

    def test_bool_true_raises_type_error(self):
        """True (bool) must raise TypeError even though bool is a subclass of int."""
        with pytest.raises(TypeError, match="numeric type"):
            mpg_to_kml(True)

    def test_bool_false_raises_type_error(self):
        """False (bool) must raise TypeError."""
        with pytest.raises(TypeError, match="numeric type"):
            mpg_to_kml(False)

    def test_complex_raises_type_error(self):
        """Complex numbers must raise TypeError."""
        with pytest.raises(TypeError, match="numeric type"):
            mpg_to_kml(3 + 2j)

    def test_empty_string_raises_type_error(self):
        """Empty string must raise TypeError."""
        with pytest.raises(TypeError, match="numeric type"):
            mpg_to_kml("")

    def test_type_error_message_includes_type_name(self):
        """TypeError message should mention the offending type name."""
        with pytest.raises(TypeError, match="str"):
            mpg_to_kml("bad")

    def test_value_error_message_includes_value(self):
        """ValueError message should include the offending value."""
        with pytest.raises(ValueError, match="-5"):
            mpg_to_kml(-5)
