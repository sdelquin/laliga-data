# laliga-data

Scraping data from spanish football [La Liga](https://laliga.com/) website.

![LaLiga Logo](laliga-logo.png)

This is a tool entirely written in Python that allows to **scrap all player data available in the official website of the spanish football league** for the current season. At the time of writing, three competitions are available: female first division, male first division and male second division.

## Setup

Create a Python virtualenv and install requirements:

```console
$ python3.10 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Optionally, you can create a `.env` file in the working directory to overwrite settings from [settings.py](settings.py).

### Other requirements

There are few external requirements for the project to work properly:

- [geckodriver](https://github.com/mozilla/geckodriver/releases)
- [Firefox Browser](https://www.mozilla.org/firefox/download/)

## Usage

```console
$ python main.py --help
Usage: main.py [OPTIONS]

Options:
  -v, --verbose              Loglevel increased to debug.
  -n, --num_players INTEGER  Num players (per competition) to be scraped. If
                             0, all available players will be retrieved.
                             [default: 0]
  --help                     Show this message and exit.
```

A common usage would be just `python main.py -v`. It takes aproximately 2 hours to finish execution (depending on the network issues).

Once finished, a **csv file** will be present in repo containing all scraped data from players.

## Data

- Generated datasets are stored in the [datasets](datasets) folder and **updated weekly**.
- Files will have a name like `S2122-laliga-players.csv` depending on the football season.
- A description of the columns can be found in [col-specs.csv](datasets/col-specs.csv).
- Datasets are also available at [Kaggle](https://www.kaggle.com/sdelquin/laliga-data).
