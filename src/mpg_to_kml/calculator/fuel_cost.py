"""Fuel cost calculation logic."""

from mpg_to_kml.conversion import mpg_to_kml


def calculate_fuel_cost(mpg, kms_traveled, price_per_liter):
    """Calculate total fuel cost for a trip.

    Args:
        mpg (float): Fuel efficiency in miles per gallon
        kms_traveled (float): Distance traveled in kilometers
        price_per_liter (float): Price per liter of fuel

    Returns:
        tuple: (kml, liters_consumed, total_cost)
    """
    kml = mpg_to_kml(mpg)
    liters_consumed = kms_traveled / kml
    total_cost = liters_consumed * price_per_liter
    return kml, liters_consumed, total_cost
