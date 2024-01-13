import requests

from harvest_rolling.harvest_main import start_harvest_main
from sanctum_rewards.sanctum_main import start_sanctum_main
from sextant_rolling.sextant_main import start_sextant_main
from awakened_leveling.awakened_main import start_awakened_main

LEAGUE_URL = "https://api.pathofexile.com/leagues?type=main&compact=1"


def set_urls(LEAGUE_NAME):
    URLs = {
        "GEM_URL": f"https://poe.ninja/api/data/itemoverview?league={LEAGUE_NAME}&type=SkillGem",
        "BEAST_URL": f"https://poe.ninja/api/data/itemoverview?league={LEAGUE_NAME}&type=Beast",
        "CURRENCY_URL": f"https://poe.ninja/api/data/currencyoverview?league={LEAGUE_NAME}&type=Currency",
        "COMPASS_PRICES_URL": "https://raw.githubusercontent.com/The-Forbidden-Trove/tft-data-prices/master/lsc/bulk-compasses.json",
    }
    return URLs


def fetch_data(url):
    my_headers = {"user-agent": "my-app/0.0.1"}

    try:
        with requests.get(url, headers=my_headers) as response:
            response.raise_for_status()
            data = response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error occurred while fetching data: {e}")

    return data


def get_league_name():
    league_data = fetch_data("https://api.pathofexile.com/leagues?type=main&compact=1")

    for league in league_data:
        if league["endAt"] is not None:
            return league["id"]
    return None


def main():
    LEAGUE_NAME = get_league_name()
    URLs = set_urls(LEAGUE_NAME)

    start_harvest_main(LEAGUE_NAME)
    start_sanctum_main(URLs["CURRENCY_URL"])
    start_sextant_main(URLs["COMPASS_PRICES_URL"])
    start_awakened_main(URLs["GEM_URL"], URLs["BEAST_URL"], URLs["CURRENCY_URL"])


if __name__ == "__main__":
    main()
