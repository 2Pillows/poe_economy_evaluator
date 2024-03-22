# main.py

from api_data import get_api_data

from harvest_rolling.harvest_main import start_harvest_main
from sanctum_rewards.sanctum_main import start_sanctum_main
from awakened_leveling.awakened_main import start_awakened_main


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
