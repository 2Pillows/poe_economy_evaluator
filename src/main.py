from harvest_rolling.harvest_main import start_harvest_main
from sanctum_rewards.sanctum_main import start_sanctum_main
from sextant_rolling.sextant_main import start_sextant_main
from awakened_leveling.awakened_main import start_awakened_main


def main():
    start_harvest_main()
    start_sanctum_main()
    start_sextant_main()
    start_awakened_main()


if __name__ == "__main__":
    main()
