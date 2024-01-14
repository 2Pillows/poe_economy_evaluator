# harvest_main.py

import os

from harvest_rolling.harvest_calculator import filter_types, start_calculations

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "harvest_rolling.txt")


def clear_file(file_destination):
    with open(file_destination, "w") as file:
        pass


def get_lifeforce_per_chaos(CURRENCY_DATA):
    lifeforce_types = {
        "yellow": "Vivid Crystallised Lifeforce",
        "red": "Wild Crystallised Lifeforce",
        "blue": "Primal Crystallised Lifeforce",
    }

    lifeforce_per_chaos = {
        color: next(
            (
                (1 / currency_item["receive"]["value"])
                for currency_item in CURRENCY_DATA
                if lifeforce_type in currency_item["currencyTypeName"]
            ),
            None,
        )
        for color, lifeforce_type in lifeforce_types.items()
    }

    return lifeforce_per_chaos


def get_average_prices(SCARAB_DATA, ESSENCE_DATA, DELIRIUMORB_DATA):
    price_types = {
        "Scarab": {
            "data": SCARAB_DATA,
            "types": [
                "Winged",
                "Gilded",
                "Polished",
            ],
        },
        "Essence": {
            "data": ESSENCE_DATA,
            "types": [
                "Deafening",
                "Shrieking",
            ],
        },
        "DeliriumOrb": {
            "data": DELIRIUMORB_DATA,
            "types": [
                "Orb",
            ],
        },
    }

    average_prices = {}

    for name, data in price_types.items():
        average_prices[name] = {}
        for type in data["types"]:
            prices = [
                item["chaosValue"] for item in data["data"] if type in item["name"]
            ]
            average_prices[name][type] = sum(prices) / len(prices) if prices else 0

    return average_prices


def start_harvest_main(SCARAB_DATA, ESSENCE_DATA, DELIRIUMORB_DATA, CURRENCY_DATA):
    clear_file(RESULTS_FILE)

    lifeforce_per_chaos = get_lifeforce_per_chaos(CURRENCY_DATA)

    average_prices = get_average_prices(SCARAB_DATA, ESSENCE_DATA, DELIRIUMORB_DATA)

    ITEMS = {
        "Scarab": {
            "data": SCARAB_DATA,
            "types": ["Winged", "Gilded", "Polished"],
            "chaos_acquisition_types": average_prices["Scarab"],
            "notable_words": [0, 1],
            "lifeforce_per_reforge": 30,
            "lifeforce_used": lifeforce_per_chaos["red"],
            "stack_limit": 10,
        },
        "Essence": {
            "data": ESSENCE_DATA,
            "types": ["Deafening", "Shrieking"],
            "chaos_acquisition_types": average_prices["Essence"],
            "notable_words": [0, -1],
            "lifeforce_per_reforge": 30,
            "lifeforce_used": lifeforce_per_chaos["blue"],
            "stack_limit": 9,
        },
        "DeliriumOrb": {
            "data": DELIRIUMORB_DATA,
            "types": ["Orb"],
            "chaos_acquisition_types": average_prices["DeliriumOrb"],
            "notable_words": [0, -1],
            "lifeforce_per_reforge": 30,
            "lifeforce_used": lifeforce_per_chaos["blue"],
            "stack_limit": 10,
        },
    }

    for item_name, item_data in ITEMS.items():
        filtered_types = filter_types(
            item_data["data"], item_data["types"], item_data["notable_words"]
        )

        start_calculations(
            item_name,
            filtered_types,
            item_data["lifeforce_per_reforge"],
            item_data["lifeforce_used"],
            item_data["chaos_acquisition_types"],
            RESULTS_FILE,
            item_data["stack_limit"],
            CURRENCY_DATA,
        )
