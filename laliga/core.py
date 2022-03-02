import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from logzero import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import settings

from . import network
from .player import Player
from .utils import build_url, init_webdriver
from .wrangling import wrangle_dataframe


class LaLigaScraper:
    def __init__(
        self,
        url=settings.LALIGA_ADV_STATS_URL,
        paginator_xpath=settings.PAGINATOR_XPATH,
        paginator_top=settings.PAGINATOR_TOP,
        competitions_div_xpath=settings.COMPETITIONS_DIV_XPATH,
        competitions_ul_xpath=settings.COMPETITIONS_UL_XPATH,
        output_filepath=settings.PLAYERS_FILEPATH,
        stats_url=settings.LALIGA_STATS_URL,
    ):
        self.url = url
        self.paginator_xpath = paginator_xpath
        self.paginator_top = paginator_top
        self.competitions_div_xpath = competitions_div_xpath
        self.competitions_ul_xpath = competitions_ul_xpath
        self.output_filepath = output_filepath
        self.stats_url = stats_url
        self.current_page = 0
        self.current_competition = 0
        self.player_data = []
        self.webdriver = init_webdriver()

        logger.info(f'Moving to {self.url}')
        self.webdriver.get(self.url)

        self._accept_cookies()
        self._close_advertisement()
        self._get_season()

    def __del__(self):
        self.webdriver.quit()

    def _accept_cookies(self):
        logger.debug('Accepting cookies')
        accept_cookies_btn = network.selenium_wait(
            self.webdriver,
            EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')),
        )
        accept_cookies_btn.click()
        time.sleep(1)

    def _close_advertisement(self):
        logger.debug('Closing advertisement')
        try:
            adv_button = network.selenium_wait(
                self.webdriver,
                EC.element_to_be_clickable((By.CLASS_NAME, 'rctfl-close')),
                num_retries=0,
            )
            adv_button.click()
            time.sleep(1)
        except TimeoutException:
            logger.warning('No advertisements found')

    def _get_season(self):
        logger.info('Getting season')
        response = network.make_request(self.stats_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.season = ''.join(re.search(r'(\d\d)/(\d\d)', soup.find('h1').text).groups())

    @property
    def seasoned_output_filepath(self):
        new_file_stem = f'S{self.season}-{self.output_filepath.stem}'
        return self.output_filepath.with_stem(new_file_stem)

    def _scroll_to_paginator(self):
        logger.debug('Scrolling to paginator')
        js_code = f"window.scrollTo({{'top': {self.paginator_top}}})"
        self.webdriver.execute_script(js_code)
        time.sleep(1)

    def _load_next_players_table(self):
        paginator = network.selenium_wait(
            self.webdriver,
            EC.element_to_be_clickable((By.XPATH, self.paginator_xpath)),
        )
        for div in paginator.find_elements_by_tag_name('div'):
            page = div.text.strip()
            if page.isnumeric():
                if int(page) == self.current_page + 1:
                    self._scroll_to_paginator()
                    div.click()
                    table = network.selenium_wait(
                        self.webdriver,
                        EC.presence_of_element_located((By.TAG_NAME, 'table')),
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
        competitions_div = self.webdriver.find_element_by_xpath(self.competitions_div_xpath)
        self.webdriver.execute_script('window.scrollTo(0, 0);')
        time.sleep(1)
        competitions_div.click()
        competitions_ul = self.webdriver.find_element_by_xpath(self.competitions_ul_xpath)
        competitions = competitions_ul.find_elements_by_tag_name('li')
        if self.current_competition >= len(competitions):
            return None
        competition = competitions[self.current_competition]
        logger.info(f'Loading competition "{competition.text}"')
        actions = ActionChains(self.webdriver)
        actions.move_to_element(competitions_div)
        actions.move_by_offset(0, (self.current_competition + 1) * settings.DROPDOWN_OFFSET)
        actions.click()
        actions.perform()
        self.current_competition += 1
        return competition.text

    def get_player_data_by_competition(self, competition: str, num_players=0):
        logger.info('Getting player data')
        num_checked_players = 1
        for player_url in self.get_player_urls():
            logger.debug(f'[{num_checked_players:03d}] {player_url}')
            player = Player(player_url, competition)
            if data := player.get_data():
                self.player_data.append(data)
                if num_checked_players == num_players:
                    break
                num_checked_players += 1
            else:
                logger.error('Unable to retrieve data')

    def get_player_data(self, num_players=0):
        while competition := self._load_next_competition():
            time.sleep(10)
            self.get_player_data_by_competition(competition, num_players)

    def to_dataframe(self):
        logger.info('Converting player data to Pandas DataFrame')
        self.df = pd.DataFrame(self.player_data)

    def wrangle_dataframe(self):
        logger.info('Wrangling player dataframe')
        self.df = wrangle_dataframe(self.df)

    def to_csv(self):
        logger.info(f'Dumping player dataframe to {self.seasoned_output_filepath}')
        self.df.to_csv(self.seasoned_output_filepath, index=False)
