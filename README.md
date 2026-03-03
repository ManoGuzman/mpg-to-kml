<img src="https://img.icons8.com/?size=100&id=gic1MWHLgRmE&format=png&color=000000" alt="Logo of the project" align="right">

# MPG to KmL Calculator · [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)
> Fuel efficiency converter and cost calculator for Costa Rica

A Python utility that converts fuel efficiency from miles per gallon (MPG) to kilometers per liter (km/l) and calculates fuel costs based on current gasoline prices in Costa Rica from RECOPE.

## Installing / Getting started

Clone the repository and install dependencies:

```shell
git clone https://github.com/your/mpg_to_kml.git
cd mpg_to_kml
pip install -r requirements.txt
```

This will install the necessary dependencies (requests and lxml) for web scraping RECOPE prices and performing calculations.

## Developing

### Built With
- Python 3.8+
- requests >= 2.31.0 - HTTP library for fetching RECOPE prices
- lxml >= 4.9.0 - XML/HTML parsing library

### Prerequisites
- Python 3.8 or higher ([Download Python](https://www.python.org/downloads/))
- pip package manager (included with Python)

### Setting up Dev

Here's a brief intro about what a developer must do in order to start developing
the project further:

```shell
git clone https://github.com/your/mpg_to_kml.git
cd mpg_to_kml/
pip install -r requirements.txt
```

The project will automatically fetch current SUPER gasoline prices from RECOPE's website. If the connection fails, it falls back to a default price of ₡677.00 per liter.

### Running the Application

This is a standalone Python script. To run:

```shell
python src/mpg_to_kml.py
```

You will be prompted to enter:
1. Vehicle fuel efficiency in MPG
2. Distance traveled in kilometers

The script will display:
- Fuel efficiency conversion (MPG to km/l)
- Distance traveled
- Fuel consumption in liters
- Current SUPER gasoline price
- Total fuel cost in Costa Rican colones (₡)

**Example output:**
```
=== Calculadora de Costo de Combustible ===

Ingrese la eficiencia del vehículo (MPG): 30
Ingrese la distancia recorrida (kms): 100

==================================================
Eficiencia: 30.0 mpg = 12.75 km/l
Distancia recorrida: 100.0 km
Combustible consumido: 7.84 litros
Precio por litro: ₡677.00
Costo total: ₡5307.84
==================================================
```

### Deploying / Publishing

This is a utility script meant to be run locally. To package for distribution:

```shell
pip install build
python -m build
```

This will create a distributable package in the `dist/` directory.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](/tags).

## Configuration

You can modify the following constants in `src/mpg_to_kml.py`:

- `DEFAULT_PRICE_CRC` - Fallback price per liter if RECOPE is unavailable (default: 677.0)
- `MPG_TO_KML_FACTOR` - Conversion factor from MPG to km/l (default: 0.425144)

The script uses interactive input for:
- `mpg_value` - Vehicle fuel efficiency in miles per gallon
- `kms_traveled` - Distance traveled in kilometers

## Tests

Currently, tests are not implemented. To add tests:

```shell
pip install pytest
pytest tests/
```

Future test coverage should include:
- MPG to km/l conversion accuracy
- Fuel consumption calculations
- Price scraping functionality
- Error handling scenarios
- Input validation

## Style guide

This project follows PEP 8 style guidelines. To check code style:

```shell
pip install pylint
pylint src/mpg_to_kml.py
```

All functions include docstrings following Google style format.

## API Reference

### Functions

#### `mpg_to_kml(mpg: float) -> float`
Converts miles per gallon to kilometers per liter.

**Parameters:**
- `mpg` (float): Fuel efficiency in miles per gallon

**Returns:**
- `float`: Fuel efficiency in kilometers per liter

#### `get_recope_super_price() -> float`
Fetches current SUPER gasoline price from RECOPE website via web scraping.
Searches through all tables on the page to find rows containing "SUPER" text.
Returns fallback price if unavailable.

**Returns:**
- `float`: Price per liter of SUPER gasoline in CRC

#### `calculate_fuel_cost(mpg: float, kms_traveled: float, price_per_liter: float) -> tuple`
Calculates total fuel cost for a trip.

**Parameters:**
- `mpg` (float): Fuel efficiency in miles per gallon
- `kms_traveled` (float): Distance traveled in kilometers
- `price_per_liter` (float): Price per liter of fuel

**Returns:**
- `tuple`: (kml, liters_consumed, total_cost)

#### `get_float_input(prompt_text: str) -> float`
Get valid float input from user with validation.

**Parameters:**
- `prompt_text` (str): Prompt message to display

**Returns:**
- `float`: Valid positive float value entered by user

## Data Source

No database is used. The script fetches live data from:
- **RECOPE Costa Rica**: https://www.recope.go.cr/productos/precios-nacionales/tabla-precios/

The web scraping implementation:
- Searches through all HTML tables on the page
- Looks for rows containing "SUPER" text
- Extracts price from table cells
- Validates price is between ₡500-₡2000 for sanity checking

## Licensing

This project is licensed under the MIT License - see the LICENSE file for details.