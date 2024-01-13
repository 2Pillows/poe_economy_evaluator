# gem_prices_extract.py

import requests


def extract_gem_prices(league_name, gems_info):
    base_url = (
        f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=SkillGem"
    )

    try:
        response = requests.get(base_url)
        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data: {e}")

    # extracted_data = []
    gem_types = ["Divergent", "Anomalous", "Phantasmal"]
    for item in data["lines"]:
        if "count" in item and item["count"] < 5 or "chaosValue" not in item:
            # if "listingCount" in item and item["listingCount"] < 100:
            continue
        if "name" in item:
            if "Vaal" in item["name"]:
                item["name"] = item["name"].replace("Vaal", "").strip()

            gem_type = next(
                (gem_type for gem_type in gem_types if gem_type in item["name"]), None
            )

            # Remove the matched gem_type from item["name"]
            if gem_type is not None:
                item["name"] = item["name"].replace(gem_type, "").strip()
            else:
                gem_type = "Superior"

            name = item["name"]

        if "corrupted" in item:
            corrupted = item["corrupted"]
        else:
            corrupted = False

        if "gemLevel" in item:
            gem_level = item["gemLevel"]
        else:
            gem_level = 0

        if "gemQuality" in item:
            gem_quality = item["gemQuality"]
        else:
            gem_quality = 0

        if "chaosValue" in item:
            chaos_value = item["chaosValue"]
        # else:
        #     chaos_value = 0

        if "divineValue" in item:
            divine_value = item["divineValue"]

        if "listingCount" in item:
            listingCount = item["listingCount"]
        else:
            listingCount = 1

        # Create a dictionary to store the extracted data for each item
        # extracted_item_data = {
        #     "name": name,
        #     "type": gem_type,
        #     "listingCount": listingCount,
        #     "corrupted": corrupted,
        #     "gemLevel": gem_level,
        #     "gemQuality": gem_quality,
        #     "chaosValue": chaos_value,
        # }

        # Name
        # Type

        # Chaos_Value
        # Listing_Count
        # Corrupted
        # Gem_Level
        # Gem_Quality

        # Append the extracted data for the current item to the list
        # extracted_data.append(extracted_item_data)

        gem_key = "Vaal_" if corrupted else ""

        chaos_value_key = gem_key + "Chaos_Value"
        divine_value_key = gem_key + "Divine_Value"
        listing_count_key = gem_key + "Listing_Count"
        corrupted_key = "Corrupted"
        gem_level_key = gem_key + "Gem_Level"
        gem_quality_key = gem_key + "Gem_Quality"

        if name in gems_info and gem_type in gems_info[name]:
            if chaos_value_key not in gems_info[name][gem_type]:
                gems_info[name][gem_type][chaos_value_key] = chaos_value
                gems_info[name][gem_type][divine_value_key] = divine_value
                gems_info[name][gem_type][listing_count_key] = listingCount
                gems_info[name][gem_type][corrupted_key] = corrupted
                gems_info[name][gem_type][gem_level_key] = gem_level
                gems_info[name][gem_type][gem_quality_key] = gem_quality

            elif gems_info[name][gem_type][chaos_value_key] <= chaos_value:
                gems_info[name][gem_type][chaos_value_key] = chaos_value
                gems_info[name][gem_type][divine_value_key] = divine_value
                gems_info[name][gem_type][listing_count_key] = listingCount
                gems_info[name][gem_type][corrupted_key] = corrupted
                gems_info[name][gem_type][gem_level_key] = gem_level
                gems_info[name][gem_type][gem_quality_key] = gem_quality

    # return extracted_data


# extract_gem_prices("Crucible")
