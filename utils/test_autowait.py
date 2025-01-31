import os

import pytest
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


def test_click(driver: WebDriver):
    driver.get(f"file://{os.path.abspath('utils/autowait.html')}")
    first_button = driver.find_element(By.ID, "first")
    second_button = driver.find_element(By.ID, "second")
    first_button.click()
    second_button.click()
    assert driver.find_element(By.ID, "placeholder").text == ""


def test_send_keys(driver: WebDriver):
    driver.get(f"file://{os.path.abspath('utils/autowait.html')}")

    third_button = driver.find_element(By.ID, "third")
    third_button.click()
    input_el = driver.find_element(By.ID, "input")

    with pytest.raises(ElementNotInteractableException) as exc:
        input_el.send_keys("hello")


def test_click_auto_wait(driver: WebDriver, autowait):
    driver.get(f"file://{os.path.abspath('utils/autowait.html')}")
    first_button = driver.find_element(By.ID, "first")
    second_button = driver.find_element(By.ID, "second")
    first_button.click()
    second_button.click()
    assert driver.find_element(By.ID, "placeholder").text == "Second button works!"


def test_send_keys_auto_wait(driver: WebDriver, autowait):
    driver.get(f"file://{os.path.abspath('utils/autowait.html')}")

    third_button = driver.find_element(By.ID, "third")
    third_button.click()
    input_el = driver.find_element(By.ID, "input")
    input_el.send_keys("hello")

    assert input_el.get_attribute("value") == "hello"
