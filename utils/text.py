import re
from decimal import Decimal


def extract_decimal_prices(text: str) -> list[Decimal]:
    prices: list[Decimal] = []
    matches = re.findall(r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2}))?", text)
    for match in matches:
        prices.append(Decimal(match.replace(",", "")))

    return prices
