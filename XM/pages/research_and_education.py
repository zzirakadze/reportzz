from XM.utils.base_page import BasePage
from selenium.webdriver.common.by import By


class ResearchAndEducationPage(BasePage):
    """
    ResearchAndEducationPage class provides functions for interacting with the Research & Education page.
    """

    ECONOMIC_CALENDAR = (By.XPATH, "//a[contains(text(), 'Economic Calendar')]")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def is_present(self) -> bool:
        try:
            self.find_element(self.ECONOMIC_CALENDAR)
            return True
        except Exception as e:
            self.logger.error(
                f"An error occurred while validating Research & Education page: {e}"
            )
            return False

    def move_to_economic_calendar(self) -> None:
        self.wait_until_clickable_and_click(self.ECONOMIC_CALENDAR)
