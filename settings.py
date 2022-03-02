from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_DIR.name

LALIGA_LANGCODE = config('LALIGA_LANGCODE', default='en-ES')
LALIGA_STATS_URL = config(
    'LALIGA_STATS_URL', default=f'https://www.laliga.com/{LALIGA_LANGCODE}/stats'
)
LALIGA_ADV_STATS_URL = config(
    'LALIGA_ADV_STATS_URL',
    default=f'https://www.laliga.com/{LALIGA_LANGCODE}/advanced-stats',
)

SELENIUM_HEADLESS = config('SELENIUM_HEADLESS', default=True, cast=lambda v: bool(int(v)))

PAGINATOR_XPATH = config(
    'PAGINATOR_XPATH', default='//*[@id="__next"]/div[5]/div[4]/div/div/div'
)
PAGINATOR_TOP = config('PAGINATOR_TOP', default=1500, cast=int)
COMPETITIONS_DIV_XPATH = config(
    'COMPETITIONS_DIV_XPATH',
    default='//*[@id="__next"]/div[5]/div[1]/div/div[2]/div/div[2]/div[1]/div',
)
COMPETITIONS_UL_XPATH = config(
    'COMPETITIONS_UL_XPATH',
    default='//*[@id="__next"]/div[5]/div[1]/div/div[2]/div/div[2]/div[1]/ul',
)
SCRIPT_DATA_ID = config('SCRIPT_DATA_ID', default='__NEXT_DATA__')
DROPDOWN_OFFSET = config('DROPDOWN_OFFSET', default=30, cast=int)

DATASETS_FOLDER = config('DATASETS_FOLDER', default=PROJECT_DIR / 'datasets', cast=Path)
PLAYERS_FILEPATH = config(
    'PLAYERS_FILEPATH', default=DATASETS_FOLDER / 'laliga-players.csv', cast=Path
)

COMPETITION_COLUMN = config('COMPETITION_COLUMN', default='competition')
PLAYER_URL_COLUMN = config('PLAYER_URL_COLUMN', default='player.url')
TWITTER_BASE_URL = config('TWITTER_BASE_URL', default='https://twitter.com/')

LOGFILE = config('LOGFILE', default=PROJECT_DIR / (PROJECT_NAME + '.log'), cast=Path)
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)

REQUESTS_TIMEOUT = config('REQUESTS_TIMEOUT', default=5, cast=int)  # seconds
REQUESTS_DELAY = config('REQUESTS_DELAY', default=1, cast=int)  # seconds
REQUESTS_RETRIES = config('REQUESTS_RETRIES', default=3, cast=int)

SELENIUM_TIMEOUT = config('SELENIUM_TIMEOUT', default=30, cast=int)  # seconds
SELENIUM_DELAY = config('SELENIUM_DELAY', default=1, cast=int)  # seconds
SELENIUM_RETRIES = config('SELENIUM_RETRIES', default=3, cast=int)


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
    'team': ('player', 'team', 'nickname'),
    'team.shortname': ('player', 'team', 'shortname'),
    'team.foundation': ('player', 'team', 'foundation'),
    'team.shield': ('player', 'team', 'shield', 'resizes', 'medium'),
    'shirt_number': ('player', 'squad', 'shirt_number'),
    'position': ('player', 'squad', 'position', 'name'),
    'photo': ('player', 'photos', '001', '512x556'),
    'stadium': ('club', 'venue', 'name'),
    'stadium.image': ('club', 'venue', 'image', 'resizes', 'medium'),
}
