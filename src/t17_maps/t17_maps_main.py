# t17_maps_main.py

from api_data import API_Data

import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "t17_maps.txt")


def start_t17_maps():
    map_prices = get_map_prices()
    fragment_prices = get_fragment_prices()

    write_results(map_prices, fragment_prices)


def write_results(map_prices, fragment_prices):
    # clear file
    with open(RESULTS_FILE, "w") as file:
        pass

    # write results
    with open(RESULTS_FILE, "a", encoding="utf-8") as file:
        write_section(file, "Map Prices", map_prices)
        write_section(file, "Fragment Prices", fragment_prices)

        # Profit w/ 1 fragment dropping
        write_section(
            file,
            "Map Profit w/ One Frag Dropping",
            get_map_profit(1, map_prices, fragment_prices),
        )

        # Profit w/ 2 fragments dropping
        write_section(
            file,
            "Map Profit w/ Two Frags Dropping",
            get_map_profit(2, map_prices, fragment_prices),
        )


def write_section(file, section_name, prices):
    file.write(f"\n---------- {section_name} ----------\n\n")
    for name, price in prices.items():
        file.write(f"{name}: {round(price)}c\n")


def get_map_profit(FRAGMENT_DROPS, map_prices, fragment_prices):
    all_fragment_prices = sum(fragment_prices.values())
    map_profits = {
        "Abomination": (
            FRAGMENT_DROPS
            * (
                fragment_prices["Blazing"]
                + fragment_prices["Reality"]
                + fragment_prices["Synthesising"]
                + all_fragment_prices
            )
            / 10
        )
        - map_prices["Abomination"],
        "Citadel": (
            FRAGMENT_DROPS
            * (
                fragment_prices["Cosmic"]
                + fragment_prices["Decaying"]
                + fragment_prices["Synthesising"]
                + all_fragment_prices
            )
            / 10
        )
        - map_prices["Citadel"],
        "Fortress": (
            FRAGMENT_DROPS
            * (
                fragment_prices["Cosmic"]
                + fragment_prices["Decaying"]
                + fragment_prices["Awakening"]
                + all_fragment_prices
            )
            / 10
        )
        - map_prices["Fortress"],
        "Sanctuary": (
            FRAGMENT_DROPS
            * (
                fragment_prices["Awakening"]
                + fragment_prices["Blazing"]
                + fragment_prices["Devouring"]
                + all_fragment_prices
            )
            / 10
        )
        - map_prices["Sanctuary"],
        "Ziggurat": (
            FRAGMENT_DROPS
            * (
                fragment_prices["Reality"]
                + fragment_prices["Devouring"]
                + fragment_prices["Synthesising"]
                + all_fragment_prices
            )
            / 10
        )
        - map_prices["Ziggurat"],
    }

    map_profits = dict(sorted(map_profits.items(), key=lambda x: x[1], reverse=True))

    return map_profits


def get_map_prices():
    map_names = [
        "Abomination",
        "Citadel",
        "Fortress",
        "Sanctuary",
        "Ziggurat",
    ]

    map_prices = {
        map_name: next(
            (
                map_data["chaosValue"]
                for map_data in API_Data.map_data
                if map_data["name"] == map_name + " Map"
            ),
            None,
        )
        for map_name in map_names
    }

    return map_prices


def get_fragment_prices():
    fragment_names = [
        "Reality",
        "Devouring",
        "Blazing",
        "Synthesising",
        "Awakening",
        "Decaying",
        "Cosmic",
    ]

    fragment_prices = {
        fragment_name: next(
            (
                currency["chaosEquivalent"]
                for currency in API_Data.currency_data
                if currency["currencyTypeName"] == fragment_name + " Fragment"
            ),
            None,
        )
        for fragment_name in fragment_names
    }

    return fragment_prices
