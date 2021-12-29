from laliga.core import LaLigaScraper

scraper = LaLigaScraper()
scraper.get_player_data()
scraper.to_dataframe()
scraper.to_csv()
