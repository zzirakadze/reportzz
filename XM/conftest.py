import logging
import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def setup_chrome(headless: bool) -> webdriver.Chrome:
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    if headless:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )
    driver.maximize_window()
    logging.info("Chrome browser setup complete.")
    return driver


def setup_firefox(headless: bool) -> webdriver.Firefox:
    firefox_options = FirefoxOptions()
    if headless:
        firefox_options.headless = True
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()), options=firefox_options
    )
    driver.maximize_window()
    logging.info("Firefox browser setup complete.")
    return driver


DRIVER_SETUP_FUNCTIONS = {"chrome": setup_chrome, "firefox": setup_firefox}


@pytest.fixture(scope="function")
def driver_instance(request):
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    headless = request.config.getoption("--headless").lower() == "true"
    if browser not in DRIVER_SETUP_FUNCTIONS:
        raise ValueError(f"Unsupported browser: {browser}")
    driver = DRIVER_SETUP_FUNCTIONS[browser](headless)
    driver.get(url)
    yield driver
    driver.quit()


def pytest_addoption(parser) -> None:
    load_dotenv()
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Choose the browser to run the tests on",
    )
    parser.addoption(
        "--url",
        action="store",
        default=os.getenv("BASE_URL"),
        help="Choose the url to run the tests on",
    )
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Choose the headless mode to run the tests on",
    )
    parser.addoption(
        "--reruns",
        action="store",
        default=0,
        help="Choose the number of times to rerun failed tests",
    )
