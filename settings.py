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
