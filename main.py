import logzero
import typer

from laliga.core import LaLigaScraper
from laliga.utils import init_logger

app = typer.Typer(add_completion=False)
logger = init_logger()


@app.command()
def run(
    verbose: bool = typer.Option(
        False, '--verbose', '-v', show_default=False, help='Loglevel increased to debug.'
    ),
    num_players: int = typer.Option(
        0,
        '--num_players',
        '-n',
        help='Num players (per competition) to be scraped. '
        'If 0, all available players will be retrieved.',
    ),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)

    scraper = LaLigaScraper()
    scraper.get_player_data(num_players)
    scraper.to_dataframe()
    scraper.wrangle_dataframe()
    scraper.to_csv()


if __name__ == "__main__":
    app()
