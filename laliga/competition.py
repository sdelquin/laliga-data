import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
from laliga import utils
from laliga.player import Player


class Competition:
    def __init__(
        self,
        url=settings.LALIGA_DATA_URL,
        paginator_xpath=settings.PAGINATOR_XPATH,
        competitions_div_xpath=settings.COMPETITIONS_DIV_XPATH,
        competitions_ul_xpath=settings.COMPETITIONS_UL_XPATH,
    ):
        self.url = url
        self.current_page = 0
        self.paginator_xpath = paginator_xpath
        self.competitions_div_xpath = competitions_div_xpath
        self.competitions_ul_xpath = competitions_ul_xpath
        self.player_data = []
        self.current_competition = 0
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

    def load_next_competition(self):
        self.webdriver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        actions = ActionChains(self.webdriver)
        competitions_div = self.webdriver.find_element_by_xpath(self.competitions_div_xpath)
        competitions_div.click()
        competitions_ul = self.webdriver.find_element_by_xpath(self.competitions_ul_xpath)
        competitions = competitions_ul.find_elements_by_tag_name('li')
        if self.current_competition >= len(competitions):
            return None
        competition = competitions[self.current_competition]
        actions.move_to_element(competitions_div)
        actions.move_by_offset(0, (self.current_competition + 1) * settings.DROPDOWN_OFFSET)
        actions.click()
        actions.perform()
        self.current_competition += 1
        return competition.text

    def get_player_data(self, competition: str, num_players=0):
        for i, player_url in enumerate(self.get_player_urls(), start=1):
            print(player_url)
            player = Player(player_url)
            data = player.get_data()
            data['competition'] = competition
            self.player_data.append(data)
            if i == num_players:
                break

    def get_competition_data(self, num_players=0):
        while competition := self.load_next_competition():
            self.get_player_data(competition, num_players)

    def to_csv(self, output_filepath=settings.DF_OUTPUT_FILEPATH):
        df = pd.DataFrame(self.player_data)
        df.to_csv(output_filepath, index=False)
