import json
import os

target_keys = ["Assuming_", "Profit_", "Upfront_"]


def convert_json(gem_list, file_name):
    with open(file_name, "w") as file:
        json.dump(gem_list, file)


def create_json(file_name, source_data):
    output_file = f"./data_files/output_jsons/{file_name}.json"

    target_dict = {
        item: {
            key: value
            for key, value in source_data[item].items()
            if any(pattern in key for pattern in target_keys)
        }
        for item in source_data
    }

    convert_json(target_dict, output_file)
    os.system("start " + output_file)
