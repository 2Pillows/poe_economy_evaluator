# sextant_main.py

import os

MIN_PROFIT = 10
COMPASS_COST = 1

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "sextant_rolling.txt")
MODIFIER_FILE = os.path.join(CUR_DIR, "modifier_weights.txt")


def get_compass_data(file):
    compass_data = {}

    with open(file, "r") as file:
        current_compass = None

        for line in file:
            line = line.strip()
            if line == "":
                continue

            if line.endswith(":"):
                current_compass = line[:-1]
                compass_data[current_compass] = {}
            else:
                key, value = line.split(":")
                key = key.strip()
                value = int(value.strip())

                compass_data[current_compass][key] = value

    return compass_data


def calculate_blockers(compass_data):
    shrine_mods = [value for name, value in compass_data.items() if "Shrine" in name]
    avg_shrine_value = sum(shrine_mods) / len(shrine_mods)
    barrel_mods = [value for name, value in compass_data.items() if "Barrel" in name]
    avg_barrel_value = sum(barrel_mods) / len(barrel_mods)

    compass_data["Shrine"] = avg_shrine_value
    compass_data["Barrel"] = avg_barrel_value

    sorted_items = sorted(compass_data.items(), key=lambda item: item[1])

    lowest_4_values = [item[1] for item in sorted_items[:3]]

    lowest_x_objects = [item for item in sorted_items if item[1] in lowest_4_values]

    lowest_values = dict(sorted_items[:3])
    lowest_x = dict(lowest_x_objects)

    return lowest_values, lowest_x


def write_to_file(
    file_name,
    lowest_mods,
    unblocked_mods,
    unblocked_average,
    valuable_mods,
    valuable_average,
    sextant_chaos,
    divine_chaos,
):
    with open(file_name, "w") as file:
        file.write(f"\nChaos per Sextant: {sextant_chaos}")
        file.write(f"\nSextant per Div:   {round(divine_chaos/sextant_chaos, 2)}\n")

        file.write(f"\nMin {MIN_PROFIT}c Profit per Roll: {valuable_average}")
        file.write(
            f"\nMin {MIN_PROFIT}c Profit per Div:  {round(divine_chaos/sextant_chaos * valuable_average, 2)}\n"
        )

        file.write(f"\nAll Profit per Roll:     {unblocked_average}")
        file.write(
            f"\nAll Profit per Div:      {round(divine_chaos/sextant_chaos * unblocked_average, 2)}\n\n"
        )

        file.write(f"-----Min {MIN_PROFIT}c Modifiers-----\n")
        for name, value in valuable_mods.items():
            formatted_line = f"{name:35} | {value.get('chaos'):10}"
            file.write(formatted_line + "\n")
        file.write(f"{MIN_PROFIT}c Mods: {len(valuable_mods)} / {len(unblocked_mods)}")

        file.write("\n\n-----Blocker Modifiers-----\n")
        for name, value in lowest_mods.items():
            formatted_line = f"{name:20} | {value:10}"
            file.write(formatted_line + "\n")


def find_modifiers(compass_data, sextant_chaos):
    total_weight = sum(value.get("weight") for key, value in compass_data.items())
    total_chaos = sum(value.get("chaos") for key, value in compass_data.items())

    valuable_compass = {}

    for name, compass in compass_data.items():
        if compass.get("chaos") < MIN_PROFIT:
            continue
        compass_value = compass.get("chaos") / compass.get("weight")
        potential_value = (total_chaos - compass.get("chaos")) / (
            total_weight - compass.get("weight")
        ) - sextant_chaos
        if compass_value >= potential_value:
            valuable_compass[name] = compass
    return valuable_compass


def start_sextant_main(PRICES_DATA, CURRENCY_DATA):
    sextant_chaos = next(
        (
            item["chaosEquivalent"]
            for item in CURRENCY_DATA
            if "Awakened Sextant" in item["currencyTypeName"]
        ),
        None,
    )

    divine_chaos = next(
        (
            item["chaosEquivalent"]
            for item in CURRENCY_DATA
            if "Divine Orb" in item["currencyTypeName"]
        ),
        None,
    )

    compass_prices = {item["name"]: item for item in PRICES_DATA.get("data")}

    compass_data = {
        name: {
            "weight": value.get("weight"),
            "chaos": compass_prices[name].get("chaos"),
        }
        for name, value in get_compass_data(MODIFIER_FILE).items()
    }

    compass_value = {
        name: (MIN_PROFIT - 1 if value["chaos"] < MIN_PROFIT - 1 else value["chaos"])
        / value["weight"]
        for name, value in compass_data.items()
    }

    three_lowest_mods, all_lowest_mods = calculate_blockers(compass_value)
    unblocked_mods = {
        key: value
        for key, value in compass_data.items()
        if key not in three_lowest_mods
    }
    unblocked_total_weight = sum(
        value.get("weight") for key, value in compass_data.items()
    )

    unblocked_weighted_sum = sum(
        value.get("weight") * value.get("chaos")
        for key, value in unblocked_mods.items()
    )
    unblocked_average = round(
        unblocked_weighted_sum / unblocked_total_weight - 1 - sextant_chaos, 2
    )

    valuable_mods = find_modifiers(unblocked_mods, sextant_chaos)
    valuable_weighted_sum = sum(
        value.get("weight") * value.get("chaos")
        for key, value in compass_data.items()
        if key in valuable_mods
    )
    valuable_average = round(
        valuable_weighted_sum / unblocked_total_weight - 1 - sextant_chaos, 2
    )

    write_to_file(
        RESULTS_FILE,
        all_lowest_mods,
        unblocked_mods,
        unblocked_average,
        valuable_mods,
        valuable_average,
        sextant_chaos,
        divine_chaos,
    )
    # os.system(f"start {compass_rolling_file}")
