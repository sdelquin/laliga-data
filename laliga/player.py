import json

from bs4 import BeautifulSoup

import settings

from . import network, utils


class Player:
    def __init__(
        self, url, competition, selected_properties=settings.PLAYER_PROPS_SELECTION
    ):
        self.url = url
        self.competition = competition
        self.selected_properties = selected_properties
        self.data = {}
        self._add_custom_properties()

    def _add_custom_properties(self):
        self.data[settings.COMPETITION_COLUMN] = self.competition
        self.data[settings.PLAYER_URL_COLUMN] = self.url

    def _extract_properties(self):
        # custom properties
        for target_key, source_keys in self.selected_properties.items():
            self.data[target_key] = utils.get_value_from_nested_keys(
                self.source_properties, source_keys
            )
        # player stats
        for item in self.source_properties['playerStats']:
            self.data[item['name']] = item['stat']

    def get_data(self):
        if response := network.make_request(self.url):
            soup = BeautifulSoup(response.text, 'html.parser')
            script_contents = soup.find('script', id=settings.SCRIPT_DATA_ID).string
            source = json.loads(script_contents)
            self.source_properties = source['props']['pageProps']
            self._extract_properties()
            return self.data

    def __str__(self):
        return self.data.get('name', self.url)
