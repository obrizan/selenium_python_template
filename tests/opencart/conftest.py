import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.opencart.search_page import SearchPage


@pytest.fixture(scope="module")
def search_page(driver: WebDriver) -> SearchPage:
    sp = SearchPage(driver)
    sp.open()
    return sp
