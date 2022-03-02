import time

import requests
import user_agent
from logzero import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox as FirefoxWebDriver
from selenium.webdriver.support.ui import WebDriverWait

import settings


def get_user_agent_header():
    return {'User-Agent': user_agent.generate_user_agent()}


def make_request(
    url,
    method='get',
    include_user_agent=True,
    timeout=settings.REQUESTS_TIMEOUT,
    num_retries=settings.REQUESTS_RETRIES,
    req_delay=settings.REQUESTS_DELAY,
):
    logger.debug(f'Requesting {url}')

    req = getattr(requests, method)
    retry = 0
    while True:
        try:
            headers = get_user_agent_header() if include_user_agent else {}
            response = req(url, headers=headers, timeout=timeout)
        except requests.exceptions.ReadTimeout as err:
            logger.error(err)
        else:
            logger.debug(f'Response status code: {response.status_code}')
            if response.status_code // 100 == 2:  # 2XX
                return response
        logger.debug(f'Request delay: {req_delay} seconds')
        time.sleep(req_delay)
        if retry >= num_retries:
            break
        retry += 1
        logger.debug(f'Network retry {retry}')


def selenium_wait(
    driver: FirefoxWebDriver,
    until,
    timeout=settings.SELENIUM_TIMEOUT,
    num_retries=settings.SELENIUM_RETRIES,
    req_delay=settings.SELENIUM_DELAY,
):
    retry = 0
    while True:
        try:
            response = WebDriverWait(driver, timeout=timeout).until(until)
        except TimeoutException as err:
            # This exception does not include any message
            logger.error('TimeoutException by Selenium')
            if retry >= num_retries:
                raise err
        else:
            return response
        logger.debug(f'Request delay: {req_delay} seconds')
        time.sleep(req_delay)
        retry += 1
        logger.debug(f'Network retry {retry}')
        driver.refresh()
