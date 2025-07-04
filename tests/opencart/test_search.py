import pytest


def test_correct_count(search_page) -> None:
    results = search_page.get_search_results()

    assert len(results) == 12


@pytest.mark.parametrize(
    "sort_method, attr, reverse",
    [
        ("sort_price_low_high", "price", False),
        ("sort_price_high_low", "price", True),
        ("sort_name_az", "name", False),
        ("sort_name_za", "name", True),
    ],
)
def test_sorting(search_page, sort_method, attr, reverse) -> None:
    getattr(search_page, sort_method)()

    products = search_page.get_search_results()
    values = [getattr(p, attr) for p in products]

    if attr == "name":
        sorted_values = sorted(values, key=str.casefold, reverse=reverse)
    else:
        sorted_values = sorted(values, reverse=reverse)

    assert values == sorted_values
