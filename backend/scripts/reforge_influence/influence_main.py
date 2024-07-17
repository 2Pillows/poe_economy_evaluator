# main.py

from backend.scripts.api_data import API_Data
from backend.scripts.keys import Keys


RESULTS_FILE = "backend/results/influence_rolling.txt"

MIN_PROFIT = 100


class ReforgeInfluenceData:
    def __init__(self):
        keys = Keys()
        api_data = API_Data().all_data

        # ref objects used to intellisense
        self.base_type_data = api_data[keys.ALL_BASE_TYPES]
        self.blue_lifeforce_per_chaos = 1 / api_data[keys.BLUE_LIFEFORCE][keys.CHAOS]
        self.divine_cost = api_data[keys.DIVINE][keys.CHAOS]
        self.cheapest_conq_exalted_orb_cost = api_data[keys.CHEAPEST_CONQ_EXALTED_ORB][
            keys.CHAOS
        ]

        self.profitable_bases = None


def start_influnece_main():
    influence_data = ReforgeInfluenceData()

    base_data = get_base_data(influence_data)

    reforge_viable = get_reforge_bases(base_data)

    profitable_bases = find_profit(influence_data, reforge_viable)

    influence_data.profitable_bases = profitable_bases

    write_to_file(influence_data)


# sort api data to a dict
# key = base variant
# value = {"level": {"variant": [data]}}
def get_base_data(influence_data: ReforgeInfluenceData):
    keys = Keys()

    base_data = {}
    for base_name, base_items in influence_data.base_type_data.items():
        for entry in base_items:
            # need at least 5 listing to consider
            if entry[keys.COUNT] < 5:
                continue

            # get base info
            base_level = str(entry[keys.LEVEL])
            base_type = entry[keys.BASE_TYPE]

            # Initialize base_data if it doesn't exist
            if base_name not in base_data:
                base_data[base_name] = {}

            # Initialize base_level dictionary if it doesn't exist
            if base_level not in base_data[base_name]:
                base_data[base_name][base_level] = {}

                # if current type is base, add orb value tokeys.CHAOS            if base_type == "base":
                entry[keys.CHAOS] += influence_data.cheapest_conq_exalted_orb_cost

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
def find_profit(influence_data: ReforgeInfluenceData, reforge_bases):
    keys = Keys()
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
                if data[keys.CHAOS] < buy_cost:
                    buy_name = type
                    buy_cost = data[keys.CHAOS]

                if type != "base":
                    sum_influence_prices += data[keys.CHAOS]

            # find avg profit per roll
            avg_profit = (
                sum_influence_prices - influence_data.blue_lifeforce_per_chaos
            ) / 6
            if avg_profit < 0:
                continue

            profitable_variants = []
            for type, data in type_data.items():
                # if base is cheaper than avg profit or is the base, not profitable
                if data[keys.CHAOS] < avg_profit or "variant" not in data:
                    continue

                profitable_variants.append(
                    {"name": data["variant"], "price": data[keys.CHAOS]}
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


def write_to_file(influence_data: ReforgeInfluenceData):
    # clear file
    with open(RESULTS_FILE, "w") as file:
        pass

    # sort profitable bases by avg profit
    influence_data.profitable_bases = dict(
        sorted(
            influence_data.profitable_bases.items(),
            key=lambda x: max(subdict["avg profit"] for subdict in x[1].values()),
            reverse=True,
        )
    )

    # write data to file
    with open(RESULTS_FILE, "a") as file:
        # orb_name = ", ".join(Cheapest_Orb.name)
        file.write("\n---------- Crafting Cost ----------\n\n")
        file.write(
            f"Blue Lifeforce: {round(influence_data.blue_lifeforce_per_chaos)} per chaos | {round(influence_data.blue_lifeforce_per_chaos * influence_data.divine_cost)} per div\n"
        )
        file.write(
            f"Conq Exalted Orb: {influence_data.cheapest_conq_exalted_orb_cost} chaos\n"
        )
        file.write("\n---------- Base Types ----------\n\n")

        for base_name, level_data in influence_data.profitable_bases.items():
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
                    f"\tlv. {base_level}: Avg Profit = {round(avg_profit)} c | {round(avg_profit / influence_data.divine_cost, 1)} d\n"
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


if __name__ == "__main__":
    start_influnece_main()
