# main.py

import requests

from api_urls import *

from harvest_rolling.harvest_main import start_harvest_main
from sanctum_rewards.sanctum_main import start_sanctum_main
from sextant_rolling.sextant_main import start_sextant_main
from awakened_leveling.awakened_main import start_awakened_main


def fetch_data(url):
    my_headers = get_header()

    try:
        with requests.get(url, headers=my_headers) as response:
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error occurred while fetching data: {e}")


def get_league_name():
    league_data = fetch_data(get_league_api_url())
    return next(
        (league["id"] for league in league_data if league["endAt"] is not None), None
    )


def get_api_data():
    LEAGUE_NAME = get_league_name()
    base_url = get_poe_ninja_base_url()
    url_endpoints = {
        "GEM": f"{base_url}/itemoverview?league={LEAGUE_NAME}&type=SkillGem",
        "BEAST": f"{base_url}/itemoverview?league={LEAGUE_NAME}&type=Beast",
        "CURRENCY": f"{base_url}/currencyoverview?league={LEAGUE_NAME}&type=Currency",
        "SCARAB": f"{base_url}/itemoverview?league={LEAGUE_NAME}&type=Scarab",
        "ESSENCE": f"{base_url}/itemoverview?league={LEAGUE_NAME}&type=Essence",
        "DELIRIUMORB": f"{base_url}/itemoverview?league={LEAGUE_NAME}&type=DeliriumOrb",
        "COMPASS_PRICES": get_tft_compass_data_url(),
    }

    url_data = {
        key: (
            fetch_data(endpoint)["lines"]
            if key != "COMPASS_PRICES"
            else fetch_data(endpoint)
        )
        for key, endpoint in url_endpoints.items()
    }

    return url_data


def main():
    api_data = get_api_data()

    start_harvest_main(
        api_data["SCARAB"],
        api_data["ESSENCE"],
        api_data["DELIRIUMORB"],
        api_data["CURRENCY"],
    )
    start_sanctum_main(api_data["CURRENCY"])
    start_awakened_main(api_data["GEM"], api_data["BEAST"], api_data["CURRENCY"])


if __name__ == "__main__":
    main()
