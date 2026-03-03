"""Convert MPG to km/l and calculate fuel costs.

This module provides functionality to:
- Convert fuel efficiency from miles per gallon (mpg) to kilometers per liter (km/l)
- Calculate fuel consumption based on distance traveled
- Calculate fuel cost using Costa Rica gas prices from RECOPE website
"""

import requests
from lxml import html

# Constants
MPG_TO_KML_FACTOR = 0.425144
DEFAULT_PRICE_CRC = 697.0


def mpg_to_kml(mpg):
    """Convert miles per gallon to kilometers per liter.

    Args:
        mpg (float): Fuel efficiency in miles per gallon

    Returns:
        float: Fuel efficiency in kilometers per liter
    """
    return mpg * MPG_TO_KML_FACTOR


def get_recope_super_price():
    """Fetch current SUPER gasoline price from RECOPE website.

    Returns:
        float: Price per liter of SUPER gasoline in CRC
    """
    url = "https://www.recope.go.cr/productos/precios-nacionales/tabla-precios/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        tree = html.fromstring(response.content)
        tables = tree.xpath('//table')

        for table in tables:
            rows = table.xpath('.//tr')
            for row in rows:
                cells = row.xpath('.//td')
                if not cells:
                    continue

                cell_texts = [cell.text_content().strip() for cell in cells]

                if any('SUPER' in text.upper() for text in cell_texts):
                    for cell_text in reversed(cell_texts):
                        try:
                            price_text = cell_text.replace('₡', '').replace(',', '').strip()
                            price = float(price_text)
                            if 500 <= price <= 2000:
                                return price
                        except ValueError:
                            continue

        raise ValueError("No se pudo encontrar el precio de SUPER en la tabla")

    except (requests.RequestException, ValueError, IndexError) as e:
        print(f"Error obteniendo precio de RECOPE: {e}")
        print(f"Usando precio de respaldo: ₡{DEFAULT_PRICE_CRC:.2f}")
        return DEFAULT_PRICE_CRC


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


def get_float_input(prompt_text):
    """Get valid float input from user.

    Args:
        prompt_text (str): Prompt message to display

    Returns:
        float: Valid float value entered by user
    """
    while True:
        try:
            value = float(input(prompt_text))
            if value > 0:
                return value
            print("Por favor ingrese un valor mayor a 0.")
        except ValueError:
            print("Por favor ingrese un número válido.")


def main():
    """Main function to demonstrate fuel cost calculation."""
    print("=== Calculadora de Costo de Combustible ===\n")

    mpg_value = get_float_input("Ingrese la eficiencia del vehículo (MPG): ")
    kms_traveled = get_float_input("Ingrese la distancia recorrida (kms): ")

    price_super_crc = get_recope_super_price()
    kml_value, liters_consumed, total_cost = calculate_fuel_cost(
        mpg_value, kms_traveled, price_super_crc
    )

    print(f"\n{'='*50}")
    print(f"Eficiencia: {mpg_value} mpg = {kml_value:.2f} km/l")
    print(f"Distancia recorrida: {kms_traveled} km")
    print(f"Combustible consumido: {liters_consumed:.2f} litros")
    print(f"Precio por litro: ₡{price_super_crc:.2f}")
    print(f"Costo total: ₡{total_cost:.2f}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
