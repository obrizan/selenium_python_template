import os
from typing import TypedDict

from retrying import retry

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from urllib3.exceptions import NewConnectionError
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager


class ScreenResolution(TypedDict):
    width: int
    height: int


WINDOW_SIZES: dict[str, ScreenResolution] = {
    "DESKTOP_1920X1080": {
        "width": 1920,
        "height": 1080,
    },
    "DESKTOP_1280X720": {
        "width": 1280,
        "height": 720,
    },
    "DESKTOP_1024X768": {
        "width": 1024,
        "height": 768,
    },
}


def get_window_resolution() -> ScreenResolution:
    window_config: str = os.getenv("WINDOW_RESOLUTION", "DESKTOP_1280X720").upper()
    return WINDOW_SIZES[window_config]


def get_driver_kind() -> str:
    driver_kind: str = os.getenv("SELENIUM_DRIVER_KIND", "chrome").lower()
    return driver_kind


def get_chrome_driver() -> WebDriver:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    resolution = get_window_resolution()
    driver.set_window_size(width=resolution["width"], height=resolution["height"])
    return driver


def get_firefox_driver() -> WebDriver:
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    resolution = get_window_resolution()
    driver.set_window_size(width=resolution["width"], height=resolution["height"])
    return driver


def get_safari_driver() -> WebDriver:
    options = webdriver.SafariOptions()
    driver = webdriver.Safari(options=options)
    resolution = get_window_resolution()
    driver.set_window_size(width=resolution["width"], height=resolution["height"])
    return driver


@retry(
    stop_max_attempt_number=3,
    stop_max_delay=10000,
    wait_fixed=1000,
    #    retry_on_exception=lambda e: isinstance(e, NewConnectionError) or isinstance(e, ConnectionRefusedError)
)
def get_remote_driver() -> WebDriver:
    res = get_window_resolution()
    options = Options()
    options.add_argument(f"--window-size={res['width']}, {res['height']}")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-smooth-scrolling")

    """
    I added this argument to avoid the "selenium.common.exceptions.
    WebDriverException: Message: unknown error: session deleted because of page crash"
    "This will force Chrome to use the /tmp directory instead.
    This may slow down the execution though since disk will be used instead of memory."
    https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
    """
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor=f'{os.getenv("REMOTE_DRIVER_URL", "http://localhost:3000")}/webdriver',
        options=options,
    )

    return driver


def get_driver_by_kind(kind: str) -> WebDriver:
    match kind:
        case "remote":
            return get_remote_driver()
        case "chrome":
            return get_chrome_driver()
        case "firefox":
            return get_firefox_driver()
        case "safari":
            return get_safari_driver()

    raise NotImplementedError("Getting driver for " + kind + " is not implemented yet.")


def get_driver() -> WebDriver:
    return get_driver_by_kind(get_driver_kind())
