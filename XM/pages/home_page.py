from selenium.webdriver.common.by import By
from XM.utils.base_page import BasePage
from time import sleep


class HomePage(BasePage):
    """
    HomePage class provides functions for interacting with the Home page.
    """

    RESEARCH_AND_EDUCATION = (By.CSS_SELECTOR, ".main_nav_research")

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.accept_cookies()

    def click_research_and_education(self) -> None:
        try:
            sleep(1)
            self.wait_until_clickable_and_click(self.RESEARCH_AND_EDUCATION)
        except Exception as e:
            self.logger.error(
                f"An error occurred while clicking on Research & Education: {e}"
            )
            raise
