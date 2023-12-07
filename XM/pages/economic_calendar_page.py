from __future__ import annotations
from selenium.webdriver.common.by import By
from XM.utils.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
import time


class EconomicCalendarPage(BasePage):
    """
    EconomicCalendarPage class provides functions for interacting with the Economic Calendar page.
    """

    SLIDE_TEXT = (By.CSS_SELECTOR, ".tc-finalval-tmz div.ng-star-inserted")
    SLIDER = (By.CSS_SELECTOR, ".mat-slider.mat-slider-horizontal")
    SLIDER_THUMB = (By.CSS_SELECTOR, ".mat-slider-thumb")
    CALENDAR_DATE = (By.CSS_SELECTOR, "button[aria-pressed='true'")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def is_present(self) -> bool:
        try:
            self.switch_to_iframe()
            self.find_element(self.SLIDER)
            return True
        except Exception as e:
            self.logger.error(
                f"An error occurred while validating Economic Calendar page: {e}"
            )
            return False

    def get_current_slide_text(self) -> str:
        """
        Get the text of the currently selected slide

        :return str: The text of the currently selected slide
        """
        slide_text_element = self.find_element(self.SLIDE_TEXT)
        return slide_text_element.text

    def move_slider(self, index: int) -> None:
        """
        Move the slider to the specified index

        :param index:
        :return None:
        """
        slider = self.find_element(self.SLIDER)
        max_value = int(slider.get_attribute("aria-valuemax"))

        slider_thumb = self.find_element(self.SLIDER_THUMB)

        move_ratio = index / max_value

        actions = ActionChains(self.driver)
        actions.click_and_hold(slider_thumb)
        actions.move_by_offset(slider.size["width"] * move_ratio, 0)
        actions.release()
        actions.perform()

        time.sleep(1)
        print("current slide text: ", self.get_current_slide_text())
        slider_thumb_location = slider_thumb.location
        self.logger.info(f"Slider thumb location: {slider_thumb_location}")

    def get_calendar_date(self) -> str | tuple[str, str]:
        """
        Get the date of the currently selected calendar date

        :return str: The date of the currently selected calendar date
        """

        calendar_date_element = self.find_elements(self.CALENDAR_DATE)
        if len(calendar_date_element) == 1:
            return calendar_date_element[0].get_attribute("aria-label")
        else:
            try:
                return (
                    f"('{calendar_date_element[0].get_attribute('aria-label')}',"
                    f" '{calendar_date_element[1].get_attribute('aria-label')}')"
                )
            except Exception as e:
                self.logger.error(
                    f"Unexpected range of elements returned: {calendar_date_element}"
                )
                raise e
