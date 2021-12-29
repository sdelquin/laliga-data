import time

import pandas as pd
from bs4 import BeautifulSoup
from logzero import logger
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
from laliga.player import Player
from laliga.utils import build_url, init_webdriver
from laliga.wrangling import wrangle_dataframe


class LaLigaScraper:
    def __init__(
        self,
        url=settings.LALIGA_DATA_URL,
        paginator_xpath=settings.PAGINATOR_XPATH,
        competitions_div_xpath=settings.COMPETITIONS_DIV_XPATH,
        competitions_ul_xpath=settings.COMPETITIONS_UL_XPATH,
    ):
        self.url = url
        self.paginator_xpath = paginator_xpath
        self.competitions_div_xpath = competitions_div_xpath
        self.competitions_ul_xpath = competitions_ul_xpath
        self.current_page = 0
        self.current_competition = 0
        self.player_data = []
        self.webdriver = init_webdriver()
        self._accept_cookies()

    def __del__(self):
        self.webdriver.quit()

    def _accept_cookies(self):
        logger.info(f'Moving to {self.url}')
        self.webdriver.get(self.url)
        accept_cookies_btn = WebDriverWait(self.webdriver, 10).until(
            EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
        )
        logger.debug('Accepting cookies')
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
        self.current_page = 0
        while table := self._load_next_players_table():
            logger.debug(f'Getting player urls from table in page {self.current_page}')
            soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
            for tr in soup.tbody.find_all('tr'):
                yield build_url(tr.td.a['href'])

    def _load_next_competition(self):
        self.webdriver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        actions = ActionChains(self.webdriver)
        competitions_div = self.webdriver.find_element_by_xpath(self.competitions_div_xpath)
        competitions_div.click()
        competitions_ul = self.webdriver.find_element_by_xpath(self.competitions_ul_xpath)
        competitions = competitions_ul.find_elements_by_tag_name('li')
        if self.current_competition >= len(competitions):
            return None
        competition = competitions[self.current_competition]
        logger.info(f'Loading competition "{competition.text}"')
        actions.move_to_element(competitions_div)
        actions.move_by_offset(0, (self.current_competition + 1) * settings.DROPDOWN_OFFSET)
        actions.click()
        actions.perform()
        self.current_competition += 1
        return competition.text

    def get_player_data_by_competition(self, competition: str, num_players=0):
        logger.info('Getting player data')
        for player_no, player_url in enumerate(self.get_player_urls(), start=1):
            logger.debug(f'[{player_no:03d}] {player_url}')
            player = Player(player_url, competition)
            data = player.get_data()
            self.player_data.append(data)
            if player_no == num_players:
                break

    def get_player_data(self, num_players=0):
        while competition := self._load_next_competition():
            self.get_player_data_by_competition(competition, num_players)

    def to_dataframe(self):
        logger.info('Converting player data to Pandas DataFrame')
        self.df = pd.DataFrame(self.player_data)

    def wrangle_dataframe(self):
        logger.info('Wrangling player dataframe')
        self.df = wrangle_dataframe(self.df)

    def to_csv(self, output_filepath=settings.DF_OUTPUT_FILEPATH):
        logger.info(f'Dumping player dataframe to {output_filepath}')
        self.df.to_csv(output_filepath, index=False)
