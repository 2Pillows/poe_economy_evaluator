# main.py
import os

from helper_scripts.gem_helpers.gem_data_calculate import calculate_chances
from helper_scripts.gem_helpers.gem_data_extract import extract_gem_data

from helper_scripts.profit_helpers.gem_prices_extract import extract_gem_prices
from helper_scripts.profit_helpers.gem_prices_calculate import calculate_profit

from helper_scripts.profit_helpers.lens_data_extract import extract_lens_prices

from helper_scripts.profit_helpers.profit_guaranteed_calc import (
    calculate_guaranteed_profit,
)
from helper_scripts.profit_helpers.profit_expected_calc import calculate_expected_profit

from helper_scripts.output_helpers.create_box_plot import create_graph

from helper_scripts.output_helpers.create_json_file import create_json


current_league = "Ancestor"

GEM_TYPES_LIST = ["Superior", "Divergent", "Anomalous", "Phantasmal"]

min_profit = 50
max_loss = 0


def main():
    gems_info = extract_gem_data("./data_files/source_data/gems_data.json")
    calculate_chances(gems_info, GEM_TYPES_LIST)

    extract_gem_prices(current_league, gems_info)

    cost_lens_primary, cost_lens_secondary = extract_lens_prices(current_league)

    # NEED TO CALCULATE VAAL
    calculate_profit(gems_info, cost_lens_primary, cost_lens_secondary, GEM_TYPES_LIST)

    # guaranteed_skill_gems, guaranteed_support_gems = calculate_guaranteed_profit(
    #     gems_info, min_profit, GEM_TYPES_LIST)

    expected_skill_gems, expected_support_gems = calculate_expected_profit(
        gems_info, min_profit, max_loss
    )

    # print("----------- Skill Gems -----------")
    # print_gem_list(expected_skill_gems)

    # print("----------- Support Gems -----------")
    # print_gem_list(expected_support_gems)

    # create_json("All_Gems", gems_info)

    create_graph(expected_skill_gems, GEM_TYPES_LIST)
    create_json("Skill_Gems", expected_skill_gems)

    create_graph(expected_support_gems, GEM_TYPES_LIST)
    create_json("Support_Gems", expected_support_gems)


if __name__ == "__main__":
    main()
