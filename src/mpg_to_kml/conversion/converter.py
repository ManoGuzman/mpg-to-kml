"""Unit conversion logic for fuel efficiency."""

# Conversion factor: 1 mpg = 0.425144 km/l
MPG_TO_KML_FACTOR = 0.425144


def mpg_to_kml(mpg):
    """Convert miles per gallon to kilometers per liter.

    Args:
        mpg (float): Fuel efficiency in miles per gallon

    Returns:
        float: Fuel efficiency in kilometers per liter
    """
    return mpg * MPG_TO_KML_FACTOR
