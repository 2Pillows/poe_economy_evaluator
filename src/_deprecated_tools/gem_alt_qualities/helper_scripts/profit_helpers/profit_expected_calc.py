# profit_expected_calc.py


def calculate_expected_profit(gems_info, min_profit, max_loss):
    support_gems = {}
    skill_gems = {}

    for gem_set_name, gem_set_data in gems_info.items():
        for gem_type, gem_data in gem_set_data.items():
            total_expected_profit = 0
            found_profit = 0
            found_loss = None

            for info_key, cur_gem_info in gem_data.items():
                if info_key.startswith("Chance_"):
                    chance_type = info_key.replace("Chance_", "")
                    profit_key = f"Profit_{chance_type}"
                    if profit_key in gem_data:
                        found_profit += 1
                        chance_value = cur_gem_info
                        profit_value = gem_data[profit_key]
                        temp_expected_profit = chance_value * profit_value
                        total_expected_profit += temp_expected_profit

                        if found_loss == None:
                            found_loss = profit_value
                        elif profit_value < found_loss:
                            found_loss = profit_value

            if (
                len(gem_set_data) < 2
                or found_profit != len(gem_set_data) - 1
                or total_expected_profit < min_profit
                or found_loss < max_loss
            ):
                continue

            type_gem_key = f"{gem_type} {gem_set_name}"
            if "Support" in gem_set_name:
                if type_gem_key not in support_gems:
                    support_gems[type_gem_key] = {}
                support_gems[type_gem_key] = gem_set_data[gem_type]
                support_gems[type_gem_key]["Total_Expected_Profit"] = round(
                    total_expected_profit, 2
                )
            else:
                if type_gem_key not in skill_gems:
                    skill_gems[type_gem_key] = {}
                skill_gems[type_gem_key] = gem_set_data[gem_type]
                skill_gems[type_gem_key]["Total_Expected_Profit"] = round(
                    total_expected_profit, 2
                )

    return skill_gems, support_gems
