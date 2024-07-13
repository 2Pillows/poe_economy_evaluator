# gem_data_extract.py

import json


def extract_gem_data(file_path):
    with open(file_path) as f:
        gems_data = json.load(f)

    gems_info = {}
    for gem in gems_data:
        # and "Vaal" not in gem["base_item"]["display_name"]
        if "static" in gem and "quality_stats" in gem["static"] and gem["static"]["quality_stats"]:
            if "Vaal" in gem["base_item"]["display_name"]:
                gem["base_item"]["display_name"] = gem["base_item"]["display_name"].replace(
                    "Vaal", "").strip()

            display_name = gem["base_item"]["display_name"]
            if display_name not in gems_info:
                gems_info[display_name] = {}

            for quality_stat in gem["static"]["quality_stats"]:
                set_name = quality_stat["set_name"]
                if set_name not in gems_info[display_name]:
                    gems_info[display_name][set_name] = {}

                weight = quality_stat["weight"]
                if "Weight" not in gems_info[display_name][set_name]:
                    gems_info[display_name][set_name]["Weight"] = weight

    return gems_info
