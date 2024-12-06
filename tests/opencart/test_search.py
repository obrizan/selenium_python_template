def test_correct_count(search_page) -> None:
    results = search_page.get_search_results()

    assert len(results) == 12


def test_sort_high_low(search_page) -> None:
    search_page.sort_price_high_low()

    products = search_page.get_search_results()
    prices = [product.price for product in products]
    assert prices == sorted(prices, reverse=True)


def test_sort_name_za(search_page) -> None:
    search_page.sort_name_za()

    products = search_page.get_search_results()
    names = [product.name for product in products]
    assert names == sorted(names, key=str.casefold, reverse=True)
