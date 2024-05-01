# profit_guaranteed_calc.py

def calculate_guaranteed_profit(gems_info, min_profit, GEM_TYPES_LIST):
    support_gems = {}
    skill_gems = {}

    for gem_set_name, gem_set_data in gems_info.items():
        for gem_type in GEM_TYPES_LIST:
            gem_data = gem_set_data.get(gem_type)
            if not gem_data or "Chaos_Value" not in gem_data:
                continue

            all_profit = True
            found_profit = 0
            total_guaranteed_profit = 0

            for profit_type in GEM_TYPES_LIST:
                if f"Profit_{profit_type}" in gem_data:
                    found_profit += 1
                    if gem_data[f"Profit_{profit_type}"] < 0:
                        all_profit = False
                    else:
                        chance_key = f'Chance_{profit_type}'
                        if chance_key in gem_data:
                            profit_value = gem_data[f"Profit_{profit_type}"]
                            chance_value = gem_data[chance_key]
                            temp_expected_profit = chance_value * profit_value
                            total_guaranteed_profit += temp_expected_profit

            if not all_profit or len(gem_set_data) < 2 or found_profit != len(gem_set_data) - 1 or total_guaranteed_profit < min_profit:
                continue

            if "Support" in gem_set_name:
                if gem_set_name not in support_gems:
                    support_gems[gem_set_name] = {}
                support_gems[gem_set_name][gem_type] = gem_data
                support_gems[gem_set_name][gem_type]["Total_Guaranteed_Profit"] = round(
                    total_guaranteed_profit, 2)
            else:
                if gem_set_name not in skill_gems:
                    skill_gems[gem_set_name] = {}
                skill_gems[gem_set_name][gem_type] = gem_data
                skill_gems[gem_set_name][gem_type]["Total_Guaranteed_Profit"] = round(
                    total_guaranteed_profit, 2)

    return skill_gems, support_gems
