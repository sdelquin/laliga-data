import os
import re
from urllib.parse import urljoin

import logzero
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import settings


def init_logger():
    console_logformat = (
        '%(asctime)s '
        '%(color)s'
        '[%(levelname)-8s] '
        '%(end_color)s '
        '%(message)s '
        '%(color)s'
        '(%(filename)s:%(lineno)d)'
        '%(end_color)s'
    )
    # remove colors on logfile
    file_logformat = re.sub(r'%\((end_)?color\)s', '', console_logformat)

    console_formatter = logzero.LogFormatter(fmt=console_logformat)
    file_formatter = logzero.LogFormatter(fmt=file_logformat)
    logzero.setup_default_logger(formatter=console_formatter)
    logzero.logfile(
        settings.LOGFILE,
        maxBytes=settings.LOGFILE_SIZE,
        backupCount=settings.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
    )
    return logzero.logger


def init_webdriver(headless=settings.SELENIUM_HEADLESS):
    options = Options()
    options.headless = headless
    profile = webdriver.FirefoxProfile()
    return webdriver.Firefox(
        options=options, firefox_profile=profile, service_log_path=os.devnull
    )


def build_url(path, base_url=settings.LALIGA_ADV_STATS_URL):
    return urljoin(base_url, path)


def get_value_from_nested_keys(data: dict, keys: tuple, k=0):
    if data is None:
        return data
    if len(keys) == 1:
        return data.get(keys[0])
    return get_value_from_nested_keys(data.get(keys[0]), keys[1:], k + 1)
