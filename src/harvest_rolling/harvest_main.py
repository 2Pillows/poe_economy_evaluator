# harvest_main.py

import os

from harvest_rolling.harvest_calculator import filter_types, start_calculations

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "harvest_rolling.txt")

BLUE_LIFEFORCE_PER_CHAOS = 20
RED_LIFEFORCE_PER_CHAOS = 22


def clear_file(file_destination):
    with open(file_destination, "w") as file:
        pass


def start_harvest_main(SCARAB_URL, ESSENCE_URL, DELIRIUMORB_URL):
    clear_file(RESULTS_FILE)

    ITEMS = {
        "Scarab": {
            "url": SCARAB_URL,
            "types": ["Winged", "Gilded", "Polished", "Rusted"],
            "chaos_acquisition_types": {
                "Winged": 60,
                "Gilded": 7,
                "Polished": 3,
                "Rusted": 1,
            },
            "notable_words": [0, 1],
            "lifeforce_per_reforge": 30,
            "lifeforce_used": RED_LIFEFORCE_PER_CHAOS,
            "stack_limit": 10,
        },
        "Essence": {
            "url": ESSENCE_URL,
            "types": ["Deafening", "Shrieking"],
            "chaos_acquisition_types": {
                "Deafening": 6,
                "Shrieking": 2,
            },
            "notable_words": [0, -1],
            "lifeforce_per_reforge": 30,
            "lifeforce_used": BLUE_LIFEFORCE_PER_CHAOS,
            "stack_limit": 9,
        },
        "DeliriumOrb": {
            "url": DELIRIUMORB_URL,
            "types": ["Orb"],
            "chaos_acquisition_types": {
                "Orb": 15,
            },
            "notable_words": [0, -1],
            "lifeforce_per_reforge": 30,
            "lifeforce_used": BLUE_LIFEFORCE_PER_CHAOS,
            "stack_limit": 10,
        },
    }

    for item_name, item_data in ITEMS.items():
        # object_data = fetch_data(LEAGUE_NAME, item_data["url"])
        filtered_types = filter_types(
            item_data["url"], item_data["types"], item_data["notable_words"]
        )

        start_calculations(
            item_name,
            filtered_types,
            item_data["lifeforce_per_reforge"],
            item_data["lifeforce_used"],
            item_data["chaos_acquisition_types"],
            RESULTS_FILE,
            item_data["stack_limit"],
        )
