# main.py

from harvest_rolling.harvest_main import start_harvest_main
from sanctum_rewards.sanctum_main import start_sanctum_main
from awakened_leveling.awakened_main import start_awakened_main
from reforge_influence.influence_main import start_influnece_main
from six_linking.six_linking_main import start_six_linking_main
from t17_maps.t17_maps_main import start_t17_maps
from chaos_res_crafting.chaos_res_crafting_main import start_chaos_res_crafting


def main():
    start_harvest_main()
    start_sanctum_main()
    start_awakened_main()
    start_influnece_main()
    start_six_linking_main()
    start_t17_maps()
    start_chaos_res_crafting()


if __name__ == "__main__":
    main()
