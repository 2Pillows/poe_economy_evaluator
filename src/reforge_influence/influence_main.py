# main.py

from api_data import API_Data

import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "influence_rolling.txt")

MIN_PROFIT = 100


def start_influnece_main():
    # collect and sort api data to dict with type key
    base_data = get_base_data()

    reforge_viable = get_reforge_bases(base_data)

    profitable_bases = find_profit(reforge_viable)

    write_to_file(profitable_bases)


# return cheapest exalted orb name, exalted orb price, blue juice price
class Cheapest_Orb:
    name = []
    price = float("inf")

    for orb_item in API_Data.all_exalted_orbs:
        orb_price = orb_item["chaosEquivalent"]
        orb_name = orb_item["currencyTypeName"]

        if orb_price < price:
            name = [orb_name]
            price = orb_price

        elif orb_price == price:
            name.append(orb_name)


# sort api data to a dict
# key = base variant
# value = {"level": {"variant": [data]}}
def get_base_data():
    # defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    base_data = {}
    for entry in API_Data.base_type_data:
        # need at least 5 listing to consider
        if entry["count"] < 5:
            continue

        # get base info
        base_name = entry["name"]
        base_level = str(entry["levelRequired"])
        base_type = entry.get("variant", "base")

        # skip items that have 2 influences
        if "/" in base_type:
            continue

        # Initialize base_data if it doesn't exist
        if base_name not in base_data:
            base_data[base_name] = {}

        # Initialize base_level dictionary if it doesn't exist
        if base_level not in base_data[base_name]:
            base_data[base_name][base_level] = {}

        # if current type is base, add orb value to chaosValue
        if base_type == "base":
            entry["chaosValue"] += Cheapest_Orb.price

        base_data[base_name][base_level][base_type] = entry

    return base_data


# find bases that have an influenced base to sell
def get_reforge_bases(base_data):
    reforge_bases = {}

    for base_name, level_data in base_data.items():
        for base_level, data in level_data.items():
            # need to have an influence type in keys
            # want to continue if only key is base
            if len(data) == 1 and "base" in data.keys():
                continue

            # Initialize base_data if it doesn't exist
            if base_name not in reforge_bases:
                reforge_bases[base_name] = {}

            reforge_bases[base_name][base_level] = data

    return reforge_bases


# find lowest price to buy in
# 1/6 chance to hit crusader, hunter, redeemer, warlord, shaper, or elder
# 1000 blue juice per roll
# for each of the chances, find the avg expected profit (sum - cost) / 5
# stay at roll if expected < current selling


# needs to meet lv requirements
def find_profit(reforge_bases):

    profitable_bases = {}

    # loop for all bases
    for base_name, level_data in reforge_bases.items():
        # loop for level of bases
        for base_level, type_data in level_data.items():

            # find cheapest base to buy, need to add cost of cheapest orb if base
            buy_name = ""
            buy_cost = float("inf")

            # get sum of influence bases
            sum_influence_prices = 0

            # loop through all variants of base at level
            for type, data in type_data.items():
                if data["chaosValue"] < buy_cost:
                    buy_name = type
                    buy_cost = data["chaosValue"]

                if type != "base":
                    sum_influence_prices += data["chaosValue"]

            # find avg profit per roll
            avg_profit = (sum_influence_prices - API_Data.lifeforce_blue) / 6
            if avg_profit < 0:
                continue

            profitable_variants = []
            for type, data in type_data.items():
                # if base is cheaper than avg profit or is the base, not profitable
                if data["chaosValue"] < avg_profit or "variant" not in data:
                    continue

                profitable_variants.append(
                    {"name": data["variant"], "price": data["chaosValue"]}
                )

            level_data = {
                "buy": {"name": buy_name, "price": buy_cost},
                "sell": profitable_variants,
            }

            if base_name not in profitable_bases:
                profitable_bases[base_name] = {}

            profitable_bases[base_name][base_level] = {
                "avg profit": avg_profit,
                "data": level_data,
            }

    return profitable_bases


def write_to_file(profitable_bases):
    # clear file
    with open(RESULTS_FILE, "w") as file:
        pass

    # sort profitable bases by avg profit
    profitable_bases = dict(
        sorted(
            profitable_bases.items(),
            key=lambda x: max(subdict["avg profit"] for subdict in x[1].values()),
            reverse=True,
        )
    )

    # write data to file
    with open(RESULTS_FILE, "a") as file:
        orb_name = ", ".join(Cheapest_Orb.name)
        file.write("\n---------- Crafting Cost ----------\n\n")
        file.write(
            f"Blue Lifeforce: {round(API_Data.lifeforce_blue)} per chaos | {round(API_Data.lifeforce_blue * API_Data.divine)} per div\n"
        )
        file.write(f"{orb_name}: {Cheapest_Orb.price} chaos\n")
        file.write("\n---------- Base Types ----------\n\n")

        for base_name, level_data in profitable_bases.items():
            if (
                max(data["avg profit"] for base_level, data in level_data.items())
                < MIN_PROFIT
            ):
                continue
            level_data = dict(
                sorted(
                    level_data.items(),
                    key=lambda x: x[1]["avg profit"],
                    reverse=True,
                )
            )

            file.write(f"{base_name}\n")
            for base_level, data in level_data.items():
                avg_profit = data["avg profit"]
                if avg_profit < MIN_PROFIT:
                    continue
                file.write(
                    f"\tlv. {base_level}: Avg Profit = {round(avg_profit)} c | {round(avg_profit / API_Data.divine, 1)} d\n"
                )

                buy_name = data["data"]["buy"]["name"]
                buy_price = data["data"]["buy"]["price"]
                if buy_name == "base":
                    buy_name = "Base + Orb"
                sell_names = ", ".join(
                    f"{item['name']} ({item['price']})" for item in data["data"]["sell"]
                )

                file.write(f"\t\tBuy: {buy_name} ({buy_price})\n")
                file.write(f"\t\tSell: {sell_names}\n")
                file.write("\n")
