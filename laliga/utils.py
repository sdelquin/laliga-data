import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import settings


def init_webdriver(headless=settings.SELENIUM_HEADLESS):
    options = Options()
    options.headless = headless
    profile = webdriver.FirefoxProfile()
    return webdriver.Firefox(
        options=options, firefox_profile=profile, service_log_path=os.devnull
    )
