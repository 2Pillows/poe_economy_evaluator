# t17_maps_main.py

from backend.src.api_data import API_Data, Singleton
from dataclasses import dataclass

RESULTS_FILE = "/workspaces/poe_economy_evaluator/backend/results/t17_maps.txt"


@dataclass
class T17MapData(metaclass=Singleton):
    map_prices: dict = None
    fragment_prices: dict = None
    one_frag_profit: dict = None
    two_frag_profit: dict = None

    map_data: list = None
    currency_data: list = None

    def set_api_data(self):
        api_data = API_Data()
        self.map_data = api_data.map_data
        self.currency_data = api_data.currency_data

    def set_results(
        self, _map_prices, _fragment_prices, _one_frag_profit, _two_frag_profit
    ):
        self.map_prices = _map_prices
        self.fragment_prices = _fragment_prices
        self.one_frag_profit = _one_frag_profit
        self.two_frag_profit = _two_frag_profit


def start_t17_maps():

    map_data = T17MapData()
    map_data.set_api_data()

    map_prices = get_map_prices(map_data)
    fragment_prices = get_fragment_prices(map_data)

    one_frag_profit = get_map_profit(1, map_prices, fragment_prices)
    two_frag_profit = get_map_profit(2, map_prices, fragment_prices)

    map_data.set_results(
        map_prices,
        fragment_prices,
        one_frag_profit,
        two_frag_profit,
    )

    write_results(map_data)


def write_results(map_data: T17MapData):
    # clear file
    with open(RESULTS_FILE, "w") as file:
        pass

    # write results
    with open(RESULTS_FILE, "a", encoding="utf-8") as file:
        write_section(file, "Map Prices", map_data.map_prices)
        write_section(file, "Fragment Prices", map_data.fragment_prices)

        # Profit w/ 1 fragment dropping
        write_section(
            file,
            "Map Profit w/ One Frag Dropping",
            map_data.one_frag_profit,
        )

        # Profit w/ 2 fragments dropping
        write_section(
            file,
            "Map Profit w/ Two Frags Dropping",
            map_data.two_frag_profit,
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
            )
            / 3
        )
        - map_prices["Abomination"],
        "Citadel": (
            FRAGMENT_DROPS
            * (
                fragment_prices["Cosmic"]
                + fragment_prices["Decaying"]
                + fragment_prices["Synthesising"]
            )
            / 3
        )
        - map_prices["Citadel"],
        "Fortress": (
            FRAGMENT_DROPS
            * (
                fragment_prices["Cosmic"]
                + fragment_prices["Decaying"]
                + fragment_prices["Awakening"]
            )
            / 3
        )
        - map_prices["Fortress"],
        "Sanctuary": (
            FRAGMENT_DROPS
            * (
                fragment_prices["Awakening"]
                + fragment_prices["Blazing"]
                + fragment_prices["Devouring"]
            )
            / 3
        )
        - map_prices["Sanctuary"],
        "Ziggurat": (
            FRAGMENT_DROPS
            * (
                fragment_prices["Reality"]
                + fragment_prices["Devouring"]
                + fragment_prices["Synthesising"]
            )
            / 3
        )
        - map_prices["Ziggurat"],
    }

    map_profits = dict(sorted(map_profits.items(), key=lambda x: x[1], reverse=True))

    return map_profits


def get_map_prices(map_data: T17MapData):
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
                for map_data in map_data.map_data
                if map_data["name"] == map_name + " Map"
            ),
            None,
        )
        for map_name in map_names
    }

    return map_prices


def get_fragment_prices(map_data: T17MapData):
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
                for currency in map_data.currency_data
                if currency["currencyTypeName"] == fragment_name + " Fragment"
            ),
            None,
        )
        for fragment_name in fragment_names
    }

    return fragment_prices


if __name__ == "__main__":
    start_t17_maps()
