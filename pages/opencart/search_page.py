from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from pages.opencart.model import ProductInfo
from utils.text import extract_decimal_prices


class SearchPage(BasePage):
    def get_relative_url(self) -> str:
        return "/index.php?route=product/category&path=20"

    def wait_page_is_present(self) -> None:
        pass

    def get_sort_input(self) -> WebElement:
        return self.driver.find_element(By.ID, "input-sort")

    def sort_price_low_high(self):
        select = Select(self.get_sort_input())
        select.select_by_visible_text("Price (Low > High)")

    def sort_price_high_low(self):
        select = Select(self.get_sort_input())
        select.select_by_visible_text("Price (High > Low)")

    def sort_name_az(self):
        select = Select(self.get_sort_input())
        select.select_by_visible_text("Name (A - Z)")

    def sort_name_za(self):
        select = Select(self.get_sort_input())
        select.select_by_visible_text("Name (Z - A)")

    def get_search_results(self) -> list[ProductInfo]:
        """A method that returns a list of ProductInfo models in the order they appear on the page."""
        products_tags = self.driver.find_elements(By.CLASS_NAME, "product-layout")
        products: list[ProductInfo] = []
        for product_div_tag in products_tags:
            name: str = product_div_tag.find_element(By.TAG_NAME, "h4").text
            price_text: str = product_div_tag.find_element(By.CLASS_NAME, "price").text
            product = ProductInfo(
                name=name, price=Decimal(extract_decimal_prices(price_text)[0])
            )
            products.append(product)

        return products
