# Monkey-patching WebElement methods to add waiting logic for unclickable elements.
# This patch is applied globally to all WebElement instances.
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def patched_click_factory(timeout: float):
    """
    Args:
        timeout (float): Maximum time to wait for the element to become clickable.
    """

    def patched_click(self):
        """
        Patches the WebElement's click method to wait for the element to be clickable.
        Args:
            self: WebElement object.
        """
        driver = self.parent
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(self))

        self._original_click()

    return patched_click


def patched_send_keys_factory(timeout: float):
    """
    Args:
        timeout (float): Maximum time to wait for the element to become clickable.
    """

    def patched_send_keys(self, *args, **kwargs):
        """
        Patches the WebElement's click method to wait for the element to be clickable.
        Args:
            self: WebElement object.
        """
        driver = self.parent
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(self))

        self._original_send_keys(*args, **kwargs)

    return patched_send_keys


def patched_clear_factory(timeout: float):
    """
    Args:
        timeout (float): Maximum time to wait for the element to become clickable.
    """

    def patched_clear(self, *args, **kwargs):
        """
        Patches the WebElement's clear method to wait for the element to be clickable.
        Args:
            self: WebElement object.
        """
        driver = self.parent
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(self))

        self._original_clear(*args, **kwargs)

    return patched_clear


def enable_autowait(timeout: float = 10.0) -> None:
    """
    Enables auto-waiting globally for all WebDriver.click() invokcations
    Args:
        self: WebElement object.
        timeout (float): Maximum time to wait for the element to become clickable.
    """
    assert not hasattr(WebElement, "_original_click"), "Autowait already enabled."
    assert not hasattr(WebElement, "_original_send_keys"), "Autowait already enabled."
    assert not hasattr(WebElement, "_original_clear"), "Autowait already enabled."
    WebElement._original_click = WebElement.click
    WebElement.click = patched_click_factory(timeout)
    WebElement._original_send_keys = WebElement.send_keys
    WebElement.send_keys = patched_send_keys_factory(timeout)
    WebElement._original_clear = WebElement.clear
    WebElement.clear = patched_clear_factory(timeout)


def disable_autowait() -> None:
    assert hasattr(WebElement, "_original_click"), "Autowait is not enabled."
    assert hasattr(WebElement, "_original_send_keys"), "Autowait is not enabled."
    assert hasattr(WebElement, "_original_clear"), "Autowait is not enabled."
    WebElement.click = WebElement._original_click
    del WebElement._original_click
    WebElement.send_keys = WebElement._original_send_keys
    del WebElement._original_send_keys
    WebElement.clear = WebElement._original_clear
    del WebElement._original_clear
