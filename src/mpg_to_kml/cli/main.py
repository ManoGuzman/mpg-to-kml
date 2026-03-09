"""Command-line interface for the fuel cost calculator."""

from mpg_to_kml.calculator import calculate_fuel_cost
from mpg_to_kml.pricing import get_recope_super_price


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

    print(f"\n{'=' * 50}")
    print(f"Eficiencia: {mpg_value} mpg = {kml_value:.2f} km/l")
    print(f"Distancia recorrida: {kms_traveled} km")
    print(f"Combustible consumido: {liters_consumed:.2f} litros")
    print(f"Precio por litro: ₡{price_super_crc:.2f}")
    print(f"Costo total: ₡{total_cost:.2f}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
