import json

import requests
from bs4 import BeautifulSoup

import settings
from laliga import utils


class Player:
    def __init__(self, url, selected_properties=settings.PLAYER_PROPS_SELECTION):
        self.url = url
        self.selected_properties = selected_properties

    def _extract_properties(self):
        data = {}
        # custom properties
        for target_key, source_keys in self.selected_properties.items():
            data[target_key] = utils.get_value_from_nested_keys(
                self.source_properties, source_keys
            )
        # player stats
        for item in self.source_properties['playerStats']:
            data[item['name']] = item['stat']
        return data

    def get_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_contents = soup.find('script', id=settings.SCRIPT_DATA_ID).string
        source = json.loads(script_contents)
        self.source_properties = source['props']['pageProps']
        return self._extract_properties()

    def __str__(self):
        return self.data['name']
