from typing import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from utils.autowait import enable_autowait, disable_autowait
from webdriver_factory import get_driver


@pytest.fixture(scope="module")
def driver() -> Generator[WebDriver, None, None]:
    """Returns initialized WedDriver instance."""
    drv = get_driver()
    yield drv
    drv.quit()


@pytest.fixture
def autowait() -> Generator[None, None, None]:
    enable_autowait()
    yield
    disable_autowait()
