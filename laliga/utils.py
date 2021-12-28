import os
from urllib.parse import urljoin

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


def build_url(path, base_url=settings.LALIGA_DATA_URL):
    return urljoin(base_url, path)


def get_value_from_nested_keys(data: dict, keys: tuple, k=0):
    if data is None:
        return data
    if len(keys) == 1:
        return data.get(keys[0])
    return get_value_from_nested_keys(data.get(keys[0]), keys[1:], k + 1)
