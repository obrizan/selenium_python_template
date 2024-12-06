from typing import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from webdriver_factory import get_driver


@pytest.fixture(scope="module")
def driver() -> Generator[WebDriver, None, None]:
    """Returns initialized WedDriver instance."""
    drv = get_driver()
    yield drv
    drv.quit()
