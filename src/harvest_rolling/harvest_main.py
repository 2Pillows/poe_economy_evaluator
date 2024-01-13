import requests
from harvest_rolling.harvest_calculator import filter_types, start_calculations

LEAGUE_NAME = "Affliction"
FILE_DESTINATION = "./results/harvest_rolling.txt"

BLUE_LIFEFORCE_PER_CHAOS = 20
RED_LIFEFORCE_PER_CHAOS = 22


ITEMS = {
    "Scarab": {
        "url": "Scarab",
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
        "url": "Essence",
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
        "url": "DeliriumOrb",
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


def clear_file(file_destination):
    with open(file_destination, "w") as file:
        pass


def fetch_data(league_name, object_name):
    base_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type={object_name}"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        object_data = data["lines"]
        return object_data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data: {e}")
        return []


def start_harvest_main():
    clear_file(FILE_DESTINATION)

    for item_name, item_data in ITEMS.items():
        object_data = fetch_data(LEAGUE_NAME, item_data["url"])
        filtered_types = filter_types(
            object_data, item_data["types"], item_data["notable_words"]
        )

        start_calculations(
            item_name,
            filtered_types,
            item_data["lifeforce_per_reforge"],
            item_data["lifeforce_used"],
            item_data["chaos_acquisition_types"],
            FILE_DESTINATION,
            item_data["stack_limit"],
        )
