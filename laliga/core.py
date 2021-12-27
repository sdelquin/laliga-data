import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
from laliga import utils


class Scraper:
    def __init__(
        self, url=settings.LALIGA_DATA_URL, paginator_xpath=settings.PAGINATOR_XPATH
    ):
        self.url = url
        self.current_page = 1
        self.paginator_xpath = paginator_xpath
        self.webdriver = utils.init_webdriver()
        self._accept_cookies()

    def __del__(self):
        self.webdriver.quit()

    def _accept_cookies(self):
        self.webdriver.get(self.url)
        accept_cookies_btn = WebDriverWait(self.webdriver, 10).until(
            EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
        )
        accept_cookies_btn.click()
        time.sleep(1)

    def _load_next_players_table(self):
        print(f'Page {self.current_page}')
        paginator = self.webdriver.find_element_by_xpath(self.paginator_xpath)
        for div in paginator.find_elements_by_tag_name('div'):
            page = div.text.strip()
            if page.isnumeric():
                if int(page) == self.current_page + 1:
                    div.click()
                    table = WebDriverWait(self.webdriver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'table'))
                    )
                    self.current_page += 1
                    return table

    def get_player_urls(self):
        players_urls = []
        while table := self._load_next_players_table():
            soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
            for tr in soup.tbody.find_all('tr'):
                player_url = urljoin(self.url, tr.td.a['href'])
                players_urls.append(player_url)
        return players_urls
