from laliga.core import LaLigaScraper
from laliga.utils import init_logger

logger = init_logger()

scraper = LaLigaScraper()
scraper.get_player_data(5)
scraper.to_dataframe()
scraper.to_csv()
