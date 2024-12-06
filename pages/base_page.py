import os
from abc import abstractmethod, ABC

from selenium.webdriver.remote.webdriver import WebDriver


class BasePage(ABC):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @abstractmethod
    def wait_page_is_present(self) -> None:
        """Implement in all children classes with an algorithm how to wait for complete page is loaded."""
        ...

    @abstractmethod
    def get_relative_url(self) -> str:
        """Returns relative URL of the current page."""
        ...

    def open(self) -> None:
        self.driver.get(os.environ["FRONTEND_URL"] + self.get_relative_url())
