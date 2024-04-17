# six_linking_main.py

from api_data import API_Data

import os

AVG_FUSINGS = 1244
AVG_JEWELLERS = 223

BENCH_JEWELLERS = 350
BENCH_FUSING = 1500

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "six_linking.txt")

MIN_PROFIT = 100


def start_six_linking_main():

    # Chancing jewellers on 20% qual base
    cost_sockets = {
        "jeweller": AVG_JEWELLERS * API_Data.jeweller,
        # "bench_jewller": BENCH_JEWELLERS * API_Data.jeweller,
        "omen_of_the_jeweller": API_Data.jeweller + API_Data.omen_of_the_jeweller,
        "beast": API_Data.black_morrigan
        + API_Data.craicic_shield_crab
        + (API_Data.beast_yellow * 2),
    }

    costs_linking = {
        # Chancing fusings on 20% qual base
        "fusing": AVG_FUSINGS * API_Data.fusing,
        # Using bench craft for links
        # "bench_fusing": BENCH_FUSING * API_Data.fusing,
        # Using single fusing and omen of connections
        "omen_of_connections": API_Data.fusing + API_Data.omen_of_connections,
        # Beast crafting to get max links
        "beast": API_Data.black_morrigan
        + API_Data.craicic_sand_spitter
        + (API_Data.beast_yellow * 2),
    }

    best_methods = {
        "sockets": min(cost_sockets.items(), key=lambda x: x[1]),
        "links": min(costs_linking.items(), key=lambda x: x[1]),
    }

    # now find most profitable items to six link and sell
    best_armours = find_best_armours(
        best_methods["sockets"][1] + best_methods["links"][1]
    )

    write_results(best_methods, best_armours)
    pass


def write_results(best_methods, best_armours):
    # clear file
    with open(RESULTS_FILE, "w") as file:
        pass

    # write data to file
    with open(RESULTS_FILE, "a", encoding="utf-8") as file:

        socket_name = best_methods["sockets"][0]
        socket_cost = best_methods["sockets"][1]

        link_name = best_methods["links"][0]
        link_cost = best_methods["links"][1]

        file.write("\n---------- Socket Cost ----------\n\n")
        if socket_name == "jeweller":
            file.write(
                f"Total: {socket_cost}c \n~{AVG_JEWELLERS} Jewellers: {round(1 / API_Data.jeweller)} for 1c\n"
            )

        if socket_name == "omen_of_the_jeweller":
            file.write(f"Omen of the Jeweller: {API_Data.omen_of_the_jeweller}c\n")

        if socket_name == "beast":
            file.write(
                f"Total: {socket_cost}c \nBlack Morrigan: {API_Data.black_morrigan}c \nCraicic Shield Crab: {API_Data.craicic_shield_crab}c \n2 Yellow: {API_Data.beast_yellow}c per\n"
            )

        file.write("\n---------- Linking Cost ----------\n\n")
        if link_name == "fusing":
            file.write(
                f"Total: {link_cost}c \n~{AVG_FUSINGS} Fusings: {round(1 / API_Data.fusing)} for 1c\n"
            )

        if link_name == "omen_of_connections":
            file.write(f"Omen of Connections: {API_Data.omen_of_connections}c\n")

        if link_name == "beast":
            file.write(
                f"Total: {link_cost}c \nBlack Morrigan: {API_Data.black_morrigan}c \nCraicic Sand Spitter: {API_Data.craicic_sand_spitter}c \n2 Yellow: {API_Data.beast_yellow}c per\n"
            )
        file.write("\n---------- Unique Armours ----------\n\n")

        file.write(f"{'Name':30} | {'':7} Profit {'':10} Buy {'':12} Sell\n")
        for name, info in best_armours.items():
            profit = info["profit"]
            buy = info["buy"]["chaosValue"]
            sell = info["sell"]["chaosValue"]
            if profit < 100:
                continue
            # Adjust the spacing for "Buy" and "Sell" information based on the name_width
            file.write(
                f"{name:30} | \t {round(profit):>5} | {round(profit/API_Data.divine, 1):>5}  {round(buy):>8} | {round(buy/API_Data.divine, 1):>5}  {round(sell):>8} | {round(sell/API_Data.divine, 1):>5}\n"
            )


def find_best_armours(crafting_cost):

    # for each base, find ones with highest difference between no and 6 links
    body_armours = {}

    for armour in API_Data.unique_armour_data:
        if armour["itemType"] != "Body Armour" or armour["count"] < 5:
            continue

        name = armour["name"]
        price = armour["chaosValue"]

        if name not in body_armours:
            body_armours[name] = {
                "profit": 0,
                "buy": armour,
                "sell": armour,
            }
            continue

        # Buy price is cheapest
        if body_armours[name]["buy"]["chaosValue"] > price:
            body_armours[name]["buy"] = armour
        # Sell price is highest
        elif body_armours[name]["sell"]["chaosValue"] < price:
            body_armours[name]["sell"] = armour

    for name, info in body_armours.items():
        # Find profit from subtracting base and crafting cost from selling
        info["profit"] = (
            info["sell"]["chaosValue"] - info["buy"]["chaosValue"] - crafting_cost
        )

    body_armours = dict(
        sorted(
            body_armours.items(),
            key=lambda x: x[1]["profit"],
            reverse=True,
        )
    )

    return body_armours
