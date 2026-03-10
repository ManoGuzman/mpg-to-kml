"""RECOPE fuel price scraper for Costa Rica SUPER gasoline."""

import requests
from lxml import html

# Fallback price in Costa Rican colones (CRC) when scraping fails
DEFAULT_PRICE_CRC = 697.0


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
        tables = tree.xpath("//table")

        for table in tables:
            rows = table.xpath(".//tr")
            for row in rows:
                cells = row.xpath(".//td")
                if not cells:
                    continue

                cell_texts = [cell.text_content().strip() for cell in cells]

                if any("SUPER" in text.upper() for text in cell_texts):
                    for cell_text in reversed(cell_texts):
                        try:
                            price_text = cell_text.replace("₡", "").replace(",", "").strip()
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
