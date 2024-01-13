# gem_prices_calculate.py


def calculate_profit(gems_info, cost_lens_primary, cost_lens_secondary, GEM_TYPES_LIST):
    # NEED TO CALCCULATE VAAL COSTS AND PROBABILITY

    for gem_set_name, gem_set_data in gems_info.items():
        if "Support" in gem_set_name:
            lens_type = "Secondary"
            cost_lens = cost_lens_secondary
        else:
            lens_type = "Prime"
            cost_lens = cost_lens_primary

        for cur_type in GEM_TYPES_LIST:
            cur_gem = gem_set_data.get(cur_type)

            if not cur_gem:
                continue

            if "Chaos_Value" not in cur_gem:
                continue

            cost = cur_gem["Chaos_Value"]
            cur_gem[f"Upfront_{cur_type}"] = cost + cost_lens

            for other_type in GEM_TYPES_LIST:
                if cur_type == other_type:
                    continue

                other_gem = gem_set_data.get(other_type)
                if not other_gem:
                    continue

                if "Chaos_Value" in other_gem:
                    cur_gem[f"Profit_{other_type}"] = round(
                        other_gem["Chaos_Value"] - cost - cost_lens, 2
                    )

                    cur_gem[f"Assuming_{other_type}"] = {}
                    assuming_dict = cur_gem[f"Assuming_{other_type}"]

                    if cur_gem["Divine_Value"] < 1:
                        assuming_dict[f"{cur_type}_Chaos"] = cur_gem["Chaos_Value"]
                    else:
                        assuming_dict[f"{cur_type}_Divine"] = cur_gem["Divine_Value"]

                    assuming_dict[f"Price_{lens_type}_Lens"] = cost_lens

                    if other_gem["Divine_Value"] < 1:
                        assuming_dict[f"{other_type}_Chaos"] = other_gem["Chaos_Value"]
                    else:
                        assuming_dict[f"{other_type}_Divine"] = other_gem[
                            "Divine_Value"
                        ]

                    assuming_dict[f"{other_type}_Gem_Level"] = other_gem["Gem_Level"]
                    assuming_dict[f"{other_type}_Gem_Quality"] = other_gem[
                        "Gem_Quality"
                    ]

                    assuming_dict[f"Listing_Count_{other_type}"] = other_gem[
                        "Listing_Count"
                    ]
