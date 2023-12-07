import logging
from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class BasePage:
    """
    BasePage class provides common functions for page interactions,
    such as waiting for and finding elements, clicking on elements,
    and automatically accepting cookies.

    Attributes:
        driver (WebDriver): Selenium WebDriver instance for web interactions.

    Methods:
        wait_until_clickable_and_click(locator, timeout): Clicks on an element after it becomes clickable.
        find_element(locator, timeout): Finds and returns a single web element.
        find_elements(locator, timeout): Finds and returns a list of web elements.
        accept_cookies(locator, timeout): Clicks the accept cookies button on the page.
    """

    ACCEPT_COOKIES_BUTTON = (
        By.XPATH,
        "//div[@class='col-sm-5']//button[contains(text(), 'ACCEPT ALL')]",
    )
    IFRAME = (By.ID, "iFrameResizer0")
    TABLE_CONTENT = (By.ID, "economic-calendar-list")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing {__name__} class")

    def find_element(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except Exception as e:
            self.logger.error(f"An error occurred while finding element {locator}: {e}")
            raise

    def find_elements(
        self, locator: Tuple[str, str], timeout: int = 10
    ) -> List[WebElement]:
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            self.logger.error(
                f"An error occurred while finding elements {locator}: {e}"
            )
            raise

    def wait_until_clickable_and_click(
        self, locator: Tuple[str, str], timeout: int = 10
    ):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except Exception as e:
            self.logger.error(
                f"An error occurred while waiting for element {locator} to be clickable and clicking on it: {e}"
            )
            raise

    def accept_cookies(
        self, locator: Tuple[str, str] = ACCEPT_COOKIES_BUTTON, timeout: int = 20
    ):
        try:
            self.wait_until_clickable_and_click(locator, timeout)
            self.logger.info("=== Cookies accepted ===")
        except Exception as e:
            self.logger.info(f"An error occurred while accepting cookies: {e}")

    def switch_to_iframe(self, locator: Tuple[str, str] = IFRAME, timeout: int = 20):
        try:
            iframe = self.find_element(locator, timeout)
            self.driver.switch_to.frame(iframe)
            self.logger.info("=== Switched to iframe ===")
        except Exception as e:
            self.logger.warning(f"An error occurred while switching to iframe: {e}")
            raise

    def get_element_content(self, locator: Tuple[str, str] = TABLE_CONTENT) -> str:
        sleep(1)
        element = self.find_element(locator)
        return element.text
