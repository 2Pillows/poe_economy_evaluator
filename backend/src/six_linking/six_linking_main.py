# six_linking_main.py

from backend.src.api_data import API_Data, Singleton
from dataclasses import dataclass

AVG_FUSINGS = 1244
AVG_JEWELLERS = 223

BENCH_JEWELLERS = 350
BENCH_FUSING = 1500

RESULTS_FILE = "backend/results/six_linking.txt"

MIN_PROFIT = 20


@dataclass
class SixLinkingData(metaclass=Singleton):
    best_methods: list = None
    best_armours: list = None

    jeweller: int = None
    omen_of_the_jeweller: int = None
    black_morrigan: int = None
    craicic_shield_crab: int = None
    beast_yellow: int = None
    fusing: int = None
    omen_of_connections: int = None
    craicic_sand_spitter: int = None

    unique_armour_data: list = None

    divine: int = None

    def set_api_data(self):
        api_data = API_Data()
        self.jeweller = api_data.jeweller
        self.omen_of_the_jeweller = api_data.omen_of_the_jeweller
        self.black_morrigan = api_data.black_morrigan
        self.craicic_shield_crab = api_data.craicic_shield_crab
        self.beast_yellow = api_data.beast_yellow
        self.fusing = api_data.fusing
        self.omen_of_connections = api_data.omen_of_connections
        self.craicic_sand_spitter = api_data.craicic_sand_spitter

        self.unique_armour_data = api_data.unique_armour_data

        self.divine = api_data.divine

    def set_results(cls, _best_methods, _best_armours):
        cls.best_methods = _best_methods
        cls.best_armours = _best_armours


def start_six_linking_main():

    linking_data = SixLinkingData()
    linking_data.set_api_data()

    # Chancing jewellers on 20% qual base
    cost_sockets = {
        "jeweller": AVG_JEWELLERS * linking_data.jeweller,
        # "bench_jewller": BENCH_JEWELLERS * linking_data.jeweller,
        "omen_of_the_jeweller": linking_data.jeweller
        + linking_data.omen_of_the_jeweller,
        "beast": linking_data.black_morrigan
        + linking_data.craicic_shield_crab
        + (linking_data.beast_yellow * 2),
    }

    costs_linking = {
        # Chancing fusings on 20% qual base
        "fusing": AVG_FUSINGS * linking_data.fusing,
        # Using bench craft for links
        # "bench_fusing": BENCH_FUSING * linking_data.fusing,
        # Using single fusing and omen of connections
        "omen_of_connections": linking_data.fusing + linking_data.omen_of_connections,
        # Beast crafting to get max links
        "beast": linking_data.black_morrigan
        + linking_data.craicic_sand_spitter
        + (linking_data.beast_yellow * 2),
    }

    best_methods = {
        "sockets": min(cost_sockets.items(), key=lambda x: x[1]),
        "links": min(costs_linking.items(), key=lambda x: x[1]),
    }

    # now find most profitable items to six link and sell
    best_armours = find_best_armours(
        best_methods["sockets"][1] + best_methods["links"][1], linking_data
    )

    linking_data.set_results(best_methods, best_armours)

    write_results(linking_data)


def write_results(linking_data: SixLinkingData):
    # clear file
    with open(RESULTS_FILE, "w") as file:
        pass

    # write data to file
    with open(RESULTS_FILE, "a", encoding="utf-8") as file:

        socket_name = linking_data.best_methods["sockets"][0]
        socket_cost = linking_data.best_methods["sockets"][1]

        link_name = linking_data.best_methods["links"][0]
        link_cost = linking_data.best_methods["links"][1]

        file.write("\n---------- Socket Cost ----------\n\n")
        if socket_name == "jeweller":
            file.write(
                f"Total: {socket_cost}c \n~{AVG_JEWELLERS} Jewellers: {round(1 / linking_data.jeweller)} for 1c\n"
            )

        if socket_name == "omen_of_the_jeweller":
            file.write(f"Omen of the Jeweller: {linking_data.omen_of_the_jeweller}c\n")

        if socket_name == "beast":
            file.write(
                f"Total: {socket_cost}c \nBlack Morrigan: {linking_data.black_morrigan}c \nCraicic Shield Crab: {linking_data.craicic_shield_crab}c \n2 Yellow: {linking_data.beast_yellow}c per\n"
            )

        file.write("\n---------- Linking Cost ----------\n\n")
        if link_name == "fusing":
            file.write(
                f"Total: {link_cost}c \n~{AVG_FUSINGS} Fusings: {round(1 / linking_data.fusing)} for 1c\n"
            )

        if link_name == "omen_of_connections":
            file.write(f"Omen of Connections: {linking_data.omen_of_connections}c\n")

        if link_name == "beast":
            file.write(
                f"Total: {link_cost}c \nBlack Morrigan: {linking_data.black_morrigan}c \nCraicic Sand Spitter: {linking_data.craicic_sand_spitter}c \n2 Yellow: {linking_data.beast_yellow}c per\n"
            )
        file.write("\n---------- Unique Armours ----------\n\n")

        file.write(f"{'Name':30} | {'':7} Profit {'':10} Buy {'':12} Sell\n")
        for name, info in linking_data.best_armours.items():
            profit = info["profit"]
            buy = info["buy"]["chaosValue"]
            sell = info["sell"]["chaosValue"]
            if profit < MIN_PROFIT:
                continue
            # Adjust the spacing for "Buy" and "Sell" information based on the name_width
            file.write(
                f"{name:30} | \t {round(profit):>5} | {round(profit/linking_data.divine, 1):>5}  {round(buy):>8} | {round(buy/linking_data.divine, 1):>5}  {round(sell):>8} | {round(sell/linking_data.divine, 1):>5}\n"
            )


def find_best_armours(crafting_cost, linking_data: SixLinkingData):

    # for each base, find ones with highest difference between no and 6 links
    body_armours = {}

    for armour in linking_data.unique_armour_data:
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


if __name__ == "__main__":
    start_six_linking_main()
