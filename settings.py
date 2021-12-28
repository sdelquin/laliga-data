from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_DIR.name

LALIGA_DATA_URL = config(
    'LALIGA_DATA_URL', default='https://www.laliga.com/en-ES/advanced-stats'
)
SELENIUM_HEADLESS = config('SELENIUM_HEADLESS', default=True, cast=lambda v: bool(int(v)))
PAGINATOR_XPATH = config(
    'PAGINATOR_XPATH', default='//*[@id="__next"]/div[5]/div[4]/div/div/div'
)
SCRIPT_DATA_ID = config('SCRIPT_DATA_ID', default='__NEXT_DATA__')
DF_OUTPUT_FILEPATH = config(
    'DF_OUTPUT_FILEPATH', default=PROJECT_DIR / (PROJECT_NAME + '.csv'), cast=Path
)

PLAYER_PROPS_SELECTION = {
    'id': ('player', 'id'),
    'slug': ('player', 'slug'),
    'name': ('player', 'name'),
    'nickname': ('player', 'nickname'),
    'firstname': ('player', 'firstname'),
    'lastname': ('player', 'lastname'),
    'gender': ('player', 'gender'),
    'date_of_birth': ('player', 'date_of_birth'),
    'place_of_birth': ('player', 'place_of_birth'),
    'weight': ('player', 'weight'),
    'height': ('player', 'height'),
    'international': ('player', 'international'),
    'twitter': ('player', 'twitter'),
    'instagram': ('player', 'instagram'),
    'country': ('player', 'country', 'id'),
}
