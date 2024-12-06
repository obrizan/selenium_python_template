from decimal import Decimal

from utils.text import extract_decimal_prices


def test_extract_decimal_prices() -> None:
    assert extract_decimal_prices("$2,110.00") == [Decimal(2110.0)]


def test_extract_decimal_prices_many() -> None:
    assert extract_decimal_prices("""
    $110.00 $122.00
    Ex Tax: $90.00
    $98.00 $122.00
    Ex Tax: $80.00
    $122.00
    Ex Tax: $100.00""") == [
        Decimal(110.00),
        Decimal(122.00),
        Decimal(90.00),
        Decimal(98.00),
        Decimal(122.00),
        Decimal(80.00),
        Decimal(122.00),
        Decimal(100.00),
    ]
