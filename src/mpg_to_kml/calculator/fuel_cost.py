"""Fuel cost calculation logic."""

from mpg_to_kml.conversion import mpg_to_kml


def _validate_positive_number(value, name):
    """Validate that a value is a positive numeric type.

    Args:
        value: The value to validate.
        name (str): Parameter name used in error messages.

    Raises:
        TypeError: If value is not an int or float (booleans excluded).
        ValueError: If value is zero or negative.
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{name} must be a numeric type, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def calculate_fuel_cost(mpg, kms_traveled, price_per_liter):
    """Calculate total fuel cost for a trip.

    Args:
        mpg (float): Fuel efficiency in miles per gallon. Must be positive.
        kms_traveled (float): Distance traveled in kilometers. Must be positive.
        price_per_liter (float): Price per liter of fuel. Must be positive.

    Returns:
        tuple: (kml, liters_consumed, total_cost)

    Raises:
        TypeError: If any argument is not a numeric type.
        ValueError: If any argument is zero or negative.
    """
    _validate_positive_number(mpg, "mpg")
    _validate_positive_number(kms_traveled, "kms_traveled")
    _validate_positive_number(price_per_liter, "price_per_liter")
    kml = mpg_to_kml(mpg)
    liters_consumed = kms_traveled / kml
    total_cost = liters_consumed * price_per_liter
    return kml, liters_consumed, total_cost
