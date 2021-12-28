import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
from laliga import utils
from laliga.player import Player


class Competition:
    def __init__(
        self, url=settings.LALIGA_DATA_URL, paginator_xpath=settings.PAGINATOR_XPATH
    ):
        self.url = url
        self.current_page = 0
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
        while table := self._load_next_players_table():
            soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
            for tr in soup.tbody.find_all('tr'):
                yield utils.build_url(tr.td.a['href'])

    def get_player_data(self, num_players=0):
        self.player_data = []
        for player_no, player_url in enumerate(self.get_player_urls()):
            print(player_url)
            if player_no == num_players:
                break
            player = Player(player_url)
            self.player_data.append(player.get_data())

    def to_csv(self, output_filepath=settings.DF_OUTPUT_FILEPATH):
        df = pd.DataFrame(self.player_data)
        df.to_csv(output_filepath, index=False)
