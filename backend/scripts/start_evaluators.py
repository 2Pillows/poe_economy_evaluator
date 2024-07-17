# main.py

# from backend.scripts.harvest_rolling.harvest_main import start_harvest_main
# from backend.scripts.sanctum_rewards.sanctum_main import start_sanctum_main
# from backend.scripts.awakened_leveling.awakened_main import start_awakened_main
# from backend.scripts.reforge_influence.influence_main import start_influnece_main
# from backend.scripts.six_linking.six_linking_main import start_six_linking_main
from backend.scripts.t17_maps.t17_maps_main import start_t17_maps

# from backend.scripts.chaos_res_crafting.chaos_res_crafting_main import (
#     start_chaos_res_crafting,
# )

from backend.scripts.api_data import get_api_data


# Timer to test script performance
# import time

# start_time = time.time()


def start_evaluators():

    # start_harvest_main()
    # start_sanctum_main()
    # start_awakened_main()
    # start_influnece_main()
    # start_six_linking_main()

    api_data = get_api_data()
    api_data["SkillGem"]["Awakened Enlighten Support"][0]["name"] = "test"
    print("c")

    start_t17_maps()
    # start_chaos_res_crafting()


if __name__ == "__main__":
    start_evaluators()
    # Timer for script performance
    # end_time = time.time()
    # runtime = end_time - start_time
    # print(f"Runtime: {runtime} seconds")
