from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class WaitsPage(BasePage):
    def get_relative_url(self) -> str:
        return "/education/selenium-playground-waits"

    def wait_page_is_present(self) -> None:
        pass

    def reset_all_tasks(self) -> None:
        self.driver.find_element(By.LINK_TEXT, "Reset all tasks").click()
