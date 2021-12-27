from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_DIR.name

LALIGA_DATA_URL = config(
    'LALIGA_DATA_URL', default='https://www.laliga.com/estadisticas-avanzadas'
)

SELENIUM_HEADLESS = config('SELENIUM_HEADLESS', default=True, cast=lambda v: bool(int(v)))
PAGINATOR_XPATH = config(
    'PAGINATOR_XPATH', default='//*[@id="__next"]/div[5]/div[4]/div/div/div'
)
