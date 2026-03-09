"""Unit conversion logic for fuel efficiency."""

# Conversion factor: 1 mpg = 0.425144 km/l
MPG_TO_KML_FACTOR = 0.425144


def mpg_to_kml(mpg):
    """Convert miles per gallon to kilometers per liter.

    Args:
        mpg (float): Fuel efficiency in miles per gallon. Must be a positive
            numeric value.

    Returns:
        float: Fuel efficiency in kilometers per liter

    Raises:
        TypeError: If mpg is not an int or float.
        ValueError: If mpg is zero or negative.
    """
    if not isinstance(mpg, (int, float)) or isinstance(mpg, bool):
        raise TypeError(f"mpg must be a numeric type, got {type(mpg).__name__}")
    if mpg <= 0:
        raise ValueError(f"mpg must be positive, got {mpg}")
    return mpg * MPG_TO_KML_FACTOR
