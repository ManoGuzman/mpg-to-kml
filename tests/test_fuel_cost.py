"""Unit tests for mpg_to_kml.calculator.fuel_cost module."""

import pytest
from mpg_to_kml.calculator.fuel_cost import calculate_fuel_cost
from mpg_to_kml.conversion.converter import MPG_TO_KML_FACTOR


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _expected_kml(mpg):
    return mpg * MPG_TO_KML_FACTOR


def _expected_liters(mpg, kms):
    return kms / _expected_kml(mpg)


def _expected_cost(mpg, kms, price):
    return _expected_liters(mpg, kms) * price


# ---------------------------------------------------------------------------
# Normal values
# ---------------------------------------------------------------------------


class TestCalculateFuelCostNormalValues:
    """Tests for typical, expected inputs."""

    def test_returns_tuple_of_three(self):
        """Return value is a 3-tuple."""
        result = calculate_fuel_cost(30, 100, 697.0)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_kml_component(self):
        """First element of returned tuple is the km/l value."""
        kml, _, _ = calculate_fuel_cost(30, 100, 697.0)
        assert kml == pytest.approx(_expected_kml(30))

    def test_liters_consumed_component(self):
        """Second element is litres consumed."""
        _, liters, _ = calculate_fuel_cost(30, 100, 697.0)
        assert liters == pytest.approx(_expected_liters(30, 100))

    def test_total_cost_component(self):
        """Third element is total cost in CRC."""
        _, _, cost = calculate_fuel_cost(30, 100, 697.0)
        assert cost == pytest.approx(_expected_cost(30, 100, 697.0))

    def test_float_inputs_accepted(self):
        """All float arguments should work without error."""
        kml, liters, cost = calculate_fuel_cost(28.5, 150.75, 750.5)
        assert kml == pytest.approx(_expected_kml(28.5))
        assert liters == pytest.approx(_expected_liters(28.5, 150.75))
        assert cost == pytest.approx(_expected_cost(28.5, 150.75, 750.5))

    def test_integer_inputs_accepted(self):
        """Integer arguments should work without error."""
        kml, liters, cost = calculate_fuel_cost(25, 200, 700)
        assert kml == pytest.approx(_expected_kml(25))

    def test_short_trip(self):
        """Very short distance (1 km) still produces a valid cost."""
        kml, liters, cost = calculate_fuel_cost(30, 1, 697.0)
        assert cost > 0

    def test_long_trip(self):
        """Long distance (1000 km) produces a proportionally larger cost."""
        _, _, cost_100 = calculate_fuel_cost(30, 100, 697.0)
        _, _, cost_1000 = calculate_fuel_cost(30, 1000, 697.0)
        assert cost_1000 == pytest.approx(cost_100 * 10, rel=1e-6)

    def test_high_efficiency_vehicle(self):
        """50 MPG vehicle consumes less fuel than 25 MPG for same distance."""
        _, liters_50, _ = calculate_fuel_cost(50, 200, 697.0)
        _, liters_25, _ = calculate_fuel_cost(25, 200, 697.0)
        assert liters_50 < liters_25

    def test_cost_scales_linearly_with_price(self):
        """Doubling price_per_liter must double the total cost."""
        _, _, cost1 = calculate_fuel_cost(30, 100, 500.0)
        _, _, cost2 = calculate_fuel_cost(30, 100, 1000.0)
        assert cost2 == pytest.approx(2 * cost1, rel=1e-6)

    def test_all_results_positive(self):
        """All three return values must be strictly positive."""
        kml, liters, cost = calculate_fuel_cost(30, 100, 697.0)
        assert kml > 0
        assert liters > 0
        assert cost > 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestCalculateFuelCostEdgeCases:
    """Tests for boundary and near-limit inputs."""

    def test_very_small_mpg(self):
        """Extremely inefficient vehicle (close to 0 MPG) produces a valid result."""
        kml, liters, cost = calculate_fuel_cost(1e-6, 100, 697.0)
        assert liters > 0
        assert cost > 0

    def test_very_large_mpg(self):
        """Extremely efficient vehicle produces small fuel consumption."""
        _, liters, _ = calculate_fuel_cost(1e6, 100, 697.0)
        assert liters == pytest.approx(100 / (1e6 * MPG_TO_KML_FACTOR))

    def test_very_small_distance(self):
        """1 metre trip (0.001 km) should still yield a positive cost."""
        _, _, cost = calculate_fuel_cost(30, 0.001, 697.0)
        assert cost > 0

    def test_very_large_distance(self):
        """Very long trip should scale cost proportionally."""
        _, _, cost_1 = calculate_fuel_cost(30, 1, 697.0)
        _, _, cost_1m = calculate_fuel_cost(30, 1_000_000, 697.0)
        assert cost_1m == pytest.approx(cost_1 * 1_000_000, rel=1e-6)

    def test_very_low_price(self):
        """Price just above 0 should still produce a valid positive cost."""
        _, _, cost = calculate_fuel_cost(30, 100, 1e-9)
        assert cost > 0

    def test_very_high_price(self):
        """Very high price per liter should scale cost correctly."""
        _, _, cost_low = calculate_fuel_cost(30, 100, 1.0)
        _, _, cost_high = calculate_fuel_cost(30, 100, 1e9)
        assert cost_high == pytest.approx(cost_low * 1e9, rel=1e-6)

    def test_zero_mpg_raises_value_error(self):
        """Zero MPG must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_fuel_cost(0, 100, 697.0)

    def test_zero_kms_raises_value_error(self):
        """Zero distance must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_fuel_cost(30, 0, 697.0)

    def test_zero_price_raises_value_error(self):
        """Zero price must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_fuel_cost(30, 100, 0)

    def test_negative_mpg_raises_value_error(self):
        """Negative MPG must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_fuel_cost(-30, 100, 697.0)

    def test_negative_kms_raises_value_error(self):
        """Negative distance must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_fuel_cost(30, -100, 697.0)

    def test_negative_price_raises_value_error(self):
        """Negative price must raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_fuel_cost(30, 100, -697.0)


# ---------------------------------------------------------------------------
# Unexpected / invalid input types
# ---------------------------------------------------------------------------


class TestCalculateFuelCostUnexpectedErrors:
    """Tests for invalid / unexpected argument types."""

    def test_string_mpg_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost("30", 100, 697.0)

    def test_string_kms_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(30, "100", 697.0)

    def test_string_price_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(30, 100, "697.0")

    def test_none_mpg_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(None, 100, 697.0)

    def test_none_kms_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(30, None, 697.0)

    def test_none_price_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(30, 100, None)

    def test_bool_mpg_raises_type_error(self):
        """bool is a subclass of int but must be rejected."""
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(True, 100, 697.0)

    def test_bool_kms_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(30, True, 697.0)

    def test_bool_price_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(30, 100, False)

    def test_list_mpg_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost([30], 100, 697.0)

    def test_dict_kms_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(30, {"kms": 100}, 697.0)

    def test_complex_price_raises_type_error(self):
        with pytest.raises(TypeError, match="numeric type"):
            calculate_fuel_cost(30, 100, 1 + 2j)

    def test_type_error_message_names_parameter(self):
        """TypeError message should reference which parameter is invalid."""
        with pytest.raises(TypeError) as exc_info:
            calculate_fuel_cost("bad", 100, 697.0)
        assert "mpg" in str(exc_info.value)

    def test_value_error_message_names_parameter(self):
        """ValueError message should reference which parameter is invalid."""
        with pytest.raises(ValueError) as exc_info:
            calculate_fuel_cost(30, -100, 697.0)
        assert "kms_traveled" in str(exc_info.value)
