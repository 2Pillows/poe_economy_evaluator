# gem_data_calculate.py

def calculate_chances(gems_info, GEM_TYPES_LIST):
    for gem_name, gem_data in gems_info.items():
        for type_name in GEM_TYPES_LIST:
            cur_gem = gem_data.get(type_name)
            if not cur_gem:
                continue

            weight = cur_gem["Weight"]

            for other_type in GEM_TYPES_LIST:
                if other_type == type_name:
                    continue

                other_gem = gem_data.get(other_type)
                if not other_gem:
                    continue

                chance_key = f"Chance_{other_type}"
                # Chances of getting cur_gem when on other_gem
                # cur_gem[chance_key] = weight / (weight + other_gem["Weight"])

                # Chances of getting other_gem when on cur_gem
                cur_gem[chance_key] = round(other_gem["Weight"] /
                                            (weight + other_gem["Weight"]), 2)
