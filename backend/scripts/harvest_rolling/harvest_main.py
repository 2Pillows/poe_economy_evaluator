#


import math
from typing import List

from backend.scripts.api_data import API_Data
from backend.scripts.keys import Keys


RESULTS_FILE = "/workspaces/poe_economy_evaluator/backend/results/harvest_rolling.txt"


class TypeData:

    def __init__(
        self,
        name,
        weights,
        api_data,
        lifeforce,
        lifeforce_used,
    ):
        keys = Keys()

        self.name = name
        self.weights = weights
        self.lifeforce = 1 / lifeforce[keys.CHAOS]
        self.lifeforce_name = self._convert_lifeforce_name(lifeforce[keys.NAME])
        self.lifeforce_used = lifeforce_used

        self.prices = {}
        self.buy_in = float("inf")
        self.roll_names = set(self.weights.keys())

        self.stop_at = None
        self.roll_at = None

        self.avg_rolls = None

        self.total_ev = None
        self.rolls_per_div = None
        self.profit_per_div = None

        self._process_api_data(api_data)

    def _convert_lifeforce_name(self, name):
        color_name = name.split()[0]

        name_map = {"Vivid": "Yellow", "Primal": "Blue", "Wild": "Red"}

        return name_map[color_name]

    def _process_api_data(self, data):
        keys = Keys()

        for name, entry in data.items():
            price = entry[keys.CHAOS]

            name = self.roll_names.intersection(name.replace("'s", "").split())

            if name:
                self.prices[name.pop()] = price
                if price < self.buy_in:
                    self.buy_in = price
            else:
                print("no name found")


def set_harvest_rolls(keys: Keys):
    api_data = API_Data().all_data

    return [
        TypeData(
            name="Fossil",
            weights={
                "Aberrant": 10.97,
                "Pristine": 10.97,
                "Scorched": 10.97,
                "Dense": 10.97,
                "Frigid": 10.97,
                "Jagged": 10.97,
                "Metallic": 10.97,
                "Aetheric": 2.19,
                "Bound": 2.19,
                "Corroded": 2.19,
                "Deft": 2.19,
                "Fundamental": 2.19,
                "Lucent": 2.19,
                "Perfect": 2.19,
                "Prismatic": 2.19,
                "Serrated": 2.19,
                "Shuddering": 2.19,
            },
            api_data=api_data[keys.HARVEST_FOSSILS],
            lifeforce=api_data[keys.RED_LIFEFORCE],
            lifeforce_used=30,
        ),
        TypeData(
            name="Oil",
            weights={
                "Clear": 33.11,
                "Sepia": 23.18,
                "Amber": 16.56,
                "Verdant": 9.93,
                "Teal": 4.97,
                "Indigo": 3.31,
                "Azure": 3.31,
                "Violet": 2.65,
                "Crimson": 1.00,
                "Black": 0.66,
                "Opalescent": 0.66,
                "Silver": 0.33,
                "Golden": 0.33,
            },
            api_data=api_data[keys.HARVEST_OILS],
            lifeforce=api_data[keys.YELLOW_LIFEFORCE],
            lifeforce_used=30,
        ),
        TypeData(
            name="Catalyst",
            weights={
                "Intrinsic": 28.75,
                "Imbued": 14.38,
                "Noxious": 14.38,
                "Turbulent": 14.38,
                "Abrasive": 14.38,
                "Prismatic": 3.75,
                "Fertile": 3.75,
                "Tempering": 3.75,
                "Accelerating": 1.25,
                "Unstable": 1.25,
            },
            api_data=api_data[keys.HARVEST_CATALYSTS],
            lifeforce=api_data[keys.YELLOW_LIFEFORCE],
            lifeforce_used=30,
        ),
        TypeData(
            name="Essence",
            weights={
                "Anger": 1,
                "Anguish": 1,
                "Contempt": 1,
                "Doubt": 1,
                "Dread": 1,
                "Envy": 1,
                "Fear": 1,
                "Greed": 1,
                "Hatred": 1,
                "Loathing": 1,
                "Misery": 1,
                "Rage": 1,
                "Scorn": 1,
                "Sorrow": 1,
                "Spite": 1,
                "Suffering": 1,
                "Torment": 1,
                "Woe": 1,
                "Wrath": 1,
                "Zeal": 1,
            },
            api_data=api_data[keys.DEAFENING_ESSENCES],
            lifeforce=api_data[keys.BLUE_LIFEFORCE],
            lifeforce_used=30,
        ),
        TypeData(
            name="Corrupted Essence",
            weights={
                "Insanity": 1,
                "Horror": 1,
                "Delirium": 1,
                "Hysteria": 1,
            },
            api_data=api_data[keys.CORRUPTED_ESSENCES],
            lifeforce=api_data[keys.BLUE_LIFEFORCE],
            lifeforce_used=30,
        ),
        TypeData(
            name="Timeless Splinter",
            weights={
                "Eternal": 1,
                "Karui": 1,
                "Maraketh": 1,
                "Templar": 1,
                "Vaal": 1,
            },
            api_data=api_data[keys.ALL_TIMELESS_SPLINTERS],
            lifeforce=api_data[keys.BLUE_LIFEFORCE],
            lifeforce_used=4,
        ),
        TypeData(
            name="Timeless Emblem",
            weights={
                "Eternal": 1,
                "Karui": 1,
                "Maraketh": 1,
                "Templar": 1,
                "Vaal": 1,
            },
            api_data=api_data[keys.ALL_TIMELESS_EMBLEMS],
            lifeforce=api_data[keys.BLUE_LIFEFORCE],
            lifeforce_used=400,
        ),
        TypeData(
            name="Breach Splinter",
            weights={
                "Chayula": 1,
                "Esh": 1,
                "Tul": 1,
                "Uul-Netol": 1,
                "Xoph": 1,
            },
            api_data=api_data[keys.ALL_BREACH_SPLINTERS],
            lifeforce=api_data[keys.RED_LIFEFORCE],
            lifeforce_used=4,
        ),
        TypeData(
            name="Breach Stone",
            weights={
                "Chayula": 1,
                "Esh": 1,
                "Tul": 1,
                "Uul-Netol": 1,
                "Xoph": 1,
            },
            api_data=api_data[keys.ALL_BREACHSTONES],
            lifeforce=api_data[keys.RED_LIFEFORCE],
            lifeforce_used=400,
        ),
        TypeData(
            name="Delirium Orb",
            weights={
                "Armoursmith": 11.1,
                "Blacksmith": 11.1,
                "Fine": 11.1,
                "Jeweller": 11.1,
                "Diviner": 5.85,
                "Foreboding": 5.85,
                # "Imperial": 5.85,
                "Whispering": 5.85,
                "Blighted": 3.2,
                "Cartographer": 3.2,
                "Fossilised": 3.2,
                "Obscured": 3.2,
                "Skittering": 3.2,
                "Abyssal": 3.2,
                # "Amorphous": 2.6,
                "Fragmented": 2.6,
                "Singular": 2.6,
                "Thaumaturge": 2.6,
                "Timeless": 2.6,
            },
            api_data=api_data[keys.DELIRIUM_ORB_DATA],
            lifeforce=api_data[keys.BLUE_LIFEFORCE],
            lifeforce_used=30,
        ),
        TypeData(
            name="Shaper Fragment",
            weights={
                "Hydra": 1,
                "Chimera": 1,
                "Minotaur": 1,
                "Phoenix": 1,
            },
            api_data=api_data[keys.ALL_SHAPER_FRAGS],
            lifeforce=api_data[keys.RED_LIFEFORCE],
            lifeforce_used=500,
        ),
        TypeData(
            name="Elder Fragment",
            weights={
                "Purification": 1,
                "Constriction": 1,
                "Eradication": 1,
                "Enslavement": 1,
            },
            api_data=api_data[keys.ALL_ELDER_FRAGS],
            lifeforce=api_data[keys.BLUE_LIFEFORCE],
            lifeforce_used=500,
        ),
        TypeData(
            name="Conqueror Fragment",
            weights={
                "Al-Hezmin": 1,
                "Baran": 1,
                "Drox": 1,
                "Veritania": 1,
            },
            api_data=api_data[keys.ALL_CONQUEROR_FRAGS],
            lifeforce=api_data[keys.YELLOW_LIFEFORCE],
            lifeforce_used=500,
        ),
        TypeData(
            name="Sacrifice Fragment",
            weights={
                "Dusk": 1,
                "Noon": 1,
                "Dawn": 1,
                "Midnight": 1,
            },
            api_data=api_data[keys.ALL_SACRIFICE_FRAGS],
            lifeforce=api_data[keys.BLUE_LIFEFORCE],
            lifeforce_used=500,
        ),
        TypeData(
            name="Mortal Fragment",
            weights={
                "Grief": 1,
                "Ignorance": 1,
                "Hope": 1,
                "Rage": 1,
            },
            api_data=api_data[keys.ALL_MORTAL_FRAGS],
            lifeforce=api_data[keys.BLUE_LIFEFORCE],
            lifeforce_used=500,
        ),
        TypeData(
            name="Uber Elder Fragment",
            weights={
                "Knowledge": 1,
                "Shape": 1,
                "Emptiness": 1,
                "Terror": 1,
            },
            api_data=api_data[keys.ALL_UBER_ELDER_FRAGS],
            lifeforce=api_data[keys.YELLOW_LIFEFORCE],
            lifeforce_used=800,
        ),
    ]


class HarvestRollingData:
    def __init__(self, keys: Keys):
        api_data = API_Data().all_data

        self.divine_cost = api_data[keys.DIVINE][keys.CHAOS]
        self.yellow_lifeforce = 1 / api_data[keys.YELLOW_LIFEFORCE][keys.CHAOS]
        self.blue_lifeforce = 1 / api_data[keys.BLUE_LIFEFORCE][keys.CHAOS]
        self.red_lifeforce = 1 / api_data[keys.RED_LIFEFORCE][keys.CHAOS]

        self.harvest_rerolls = None


def start_harvest_main():
    keys = Keys()
    harvest_data = HarvestRollingData(keys)
    harvest_rerolls = set_harvest_rolls(keys)

    for reroll_type in harvest_rerolls:
        # if reroll_type.type == "Delirium Orb":
        #     calc_prices(reroll_type)
        calc_prices(harvest_data, reroll_type)

    harvest_rerolls = sorted(
        harvest_rerolls, key=lambda x: x.profit_per_div, reverse=True
    )

    harvest_data.harvest_rerolls = harvest_rerolls

    write_results(harvest_data)


def write_results(harvest_data: HarvestRollingData):
    with open(RESULTS_FILE, "w") as file:
        pass

    with open(RESULTS_FILE, "a") as file:
        file.write("\n---------- Lifeforce per Chaos ----------\n\n")

        file.write(
            f"{'Yellow:':8} {round(harvest_data.yellow_lifeforce)} per chaos | {round((harvest_data.yellow_lifeforce) * harvest_data.divine_cost)} per div\n"
        )
        file.write(
            f"{'Blue:':8} {round(harvest_data.blue_lifeforce)} per chaos | {round((harvest_data.blue_lifeforce) * harvest_data.divine_cost)} per div\n"
        )
        file.write(
            f"{'Red:':8} {round(harvest_data.red_lifeforce)} per chaos | {round((harvest_data.red_lifeforce) * harvest_data.divine_cost)} per div \n\n"
        )

        for reroll in harvest_data.harvest_rerolls:
            reroll: TypeData
            if reroll.profit_per_div > 0:
                file.write(f"---------- {reroll.name} ----------\n\n")

                # file.write(
                #     f"Avg Profit per Reroll: {round(reroll.total_ev, 5)}\n"
                # )
                profit_per_div = reroll.total_ev * (
                    harvest_data.divine_cost / reroll.buy_in
                )

                file.write(
                    f"Avg Profit per Divine (x{round(reroll.rolls_per_div)}): {round(profit_per_div, 2)}c \n\n"
                )

                file.write(
                    f"Buying At: {round(reroll.buy_in, 2)}c each | {round(harvest_data.divine_cost/reroll.buy_in)} per div\n"
                )
                file.write(f"Avg Rolls: {reroll.avg_rolls}\n")
                file.write(f"Lifeforce: {reroll.lifeforce_name}\n\n")
                # for name, price in type_data.stop_at.items():
                #     file.write(f"{name}: {round(type_data.prices[name])}\n")

                sell_names = ", ".join(reroll.stop_at)
                file.write(f"Sell: {sell_names}\n")

                buy_names = ", ".join(reroll.roll_at)
                file.write(f"Buy: {buy_names}\n\n")


# find rolls w/ higher price that potential prices of other rolls
def calc_prices(harvest_data: HarvestRollingData, type_data: TypeData):

    total_weight = sum(type_data.weights.values())

    lifeforce_cost = type_data.lifeforce_used / type_data.lifeforce

    stop_at = []
    roll_at = []

    total_ev = 0
    total_prob = 0

    # calculate generic and actual ev for rolling at each name
    # if generic ev > 0, roll
    # set actual_ev as value for name

    # then find the ev with the actual_ev as the value
    # get sum for actual_ev for profit

    actual_evs = {}

    for current_name, current_weight in type_data.weights.items():

        remaining_weight = total_weight - current_weight

        current_price = type_data.prices[current_name]

        current_ev = 0

        for name, weight in type_data.weights.items():
            if name == current_name:
                continue

            probability = weight / remaining_weight

            current_ev += probability * type_data.prices[name]

        generic_ev = current_ev - current_price - lifeforce_cost
        actual_ev = current_ev - type_data.buy_in - lifeforce_cost

        # Roll when generic ev is more than 0
        if generic_ev > 0:
            roll_at.append(current_name)

            actual_evs[current_name] = actual_ev

        # Stop when generic ev <= 0
        else:
            stop_at.append(current_name)

    for name in roll_at:
        weight = type_data.weights[name]

        prob = weight / total_weight

        ev = prob * actual_evs[name]

        total_prob += prob
        total_ev += ev

    type_data.stop_at = stop_at
    type_data.roll_at = roll_at

    rolls_per_div = harvest_data.divine_cost / type_data.buy_in
    profit_per_div = total_ev * rolls_per_div
    type_data.rolls_per_div = rolls_per_div
    type_data.profit_per_div = profit_per_div

    accuracy = 0.95

    type_data.avg_rolls = (
        math.ceil(math.log(1 - accuracy) / math.log(1 - total_prob))
        if total_ev > 0
        else -1
    )

    type_data.total_ev = total_ev


if __name__ == "__main__":  #
    start_harvest_main()
