#


from typing import List

from backend.scripts.api_data import API_Data, ScriptData
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
        self.lifeforce_name = lifeforce[keys.NAME]
        self.lifeforce_used = lifeforce_used

        self.prices = {}
        self.min_price = float("inf")
        self.roll_names = set(self.weights.keys())

        self._process_api_data(api_data)

    def set_valuable(self, valuable):
        self.valuable = valuable

    def set_expected_value(self, expected_value):
        api_data = API_Data().all_data
        keys = Keys()
        self.expected_value = expected_value

        # avg expected value, unsure if need to get avg of evs or just sum since probability already acounted for
        # self.profit_per_roll = sum(self.expected_value.values()) / len(
        #     self.expected_value
        # )
        self.profit_per_roll = sum(self.expected_value.values())

        self.rolls_per_div = api_data[keys.DIVINE][keys.CHAOS] / self.min_price
        self.profit_per_div = self.profit_per_roll * self.rolls_per_div

    def _process_api_data(self, data):
        keys = Keys()

        for name, entry in data.items():
            price = entry[keys.CHAOS]

            name = self.roll_names.intersection(name.replace("'s", "").split())

            if name:
                self.prices[name.pop()] = price
                if price < self.min_price:
                    self.min_price = price
            else:
                print("no name found")

    def set_avg_rolls(self, rolls):
        self.avg_rolls = rolls


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


class HarvestRollingData(ScriptData):
    def __init__(self, keys: Keys):
        api_data = API_Data().all_data

        self.divine_cost = api_data[keys.DIVINE][keys.CHAOS]
        self.lifeforce_yellow_cost = api_data[keys.YELLOW_LIFEFORCE][keys.CHAOS]
        self.lifeforce_blue_cost = api_data[keys.BLUE_LIFEFORCE][keys.CHAOS]
        self.lifeforce_red_cost = api_data[keys.RED_LIFEFORCE][keys.CHAOS]

        self.harvest_rerolls = None


def start_harvest_main():
    keys = Keys()
    harvest_data = HarvestRollingData(keys)
    harvest_rerolls = set_harvest_rolls(keys)

    for reroll_type in harvest_rerolls:
        # if reroll_type.type == "Delirium Orb":
        #     calc_prices(reroll_type)
        calc_prices(reroll_type)

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
            f"{'Yellow:':8} {round(harvest_data.lifeforce_yellow_cost)} per chaos | {round((harvest_data.lifeforce_yellow_cost) * harvest_data.divine_cost)} per div\n"
        )
        file.write(
            f"{'Blue:':8} {round(harvest_data.lifeforce_blue_cost)} per chaos | {round((harvest_data.lifeforce_blue_cost) * harvest_data.divine_cost)} per div\n"
        )
        file.write(
            f"{'Red:':8} {round(harvest_data.lifeforce_red_cost)} per chaos | {round((harvest_data.lifeforce_red_cost) * harvest_data.divine_cost)} per div \n\n"
        )

        for reroll in harvest_data.harvest_rerolls:
            if reroll.profit_per_div > 0:
                file.write(f"---------- {reroll.name} ----------\n\n")

                # file.write(
                #     f"Avg Profit per Reroll: {round(reroll.profit_per_roll, 5)}\n"
                # )
                profit_per_div = reroll.profit_per_roll * (
                    harvest_data.divine_cost / reroll.min_price
                )

                file.write(
                    f"Avg Profit per Divine (x{round(reroll.rolls_per_div)}): {round(profit_per_div, 2)}c \n\n"
                )
                file.write(f"Lifeforce: {reroll.lifeforce}\n")
                file.write(f"Avg Rolls: {reroll.avg_rolls}\n\n")
                # for name, price in type_data.valuable.items():
                #     file.write(f"{name}: {round(type_data.prices[name])}\n")

                sell_names = ", ".join(reroll.valuable.keys())
                file.write(f"Sell: {sell_names}\n")

                buy_names_set = set(reroll.expected_value.keys()) - set(
                    reroll.valuable.keys()
                )
                buy_names_sorted = sorted(
                    buy_names_set, key=lambda x: reroll.expected_value[x]
                )[:10]
                buy_names = ", ".join(buy_names_sorted)

                file.write(f"Buy: {buy_names}\n\n")


# find rolls w/ higher price that potential prices of other rolls
def calc_prices(type_data: TypeData):

    # using roll data, find percentages
    total_value = sum(type_data.weights.values())

    n = type_data.name

    # number of harvest rolls
    num_rolls = 1

    max_ev = float("-inf")
    expected_value = {}

    # (sum(product(weight * price))) = adjusted price total
    # weight * price = adjusted price
    # price total - price = price for rerolling
    # price for rerolling / chances of alternative rolls = avg price for reroll
    # avg price for reroll - reroll cost - price for item = profit

    # roll_prices = {}
    # roll_chances = {}

    # for name, count in type_data.rolls.items():
    #     roll_chances[name] = count / total_value

    # for name, price in type_data.prices.items():
    #     roll_prices[name] = roll_chances[name] * price

    # # roll info has avg price, get total
    # total_price = sum(roll_prices.values())

    # reroll_profit = {}

    # lifeforce_price = 0.32
    # for name, count in type_data.rolls.items():
    #     reroll_result = (total_price - roll_prices[name]) / (1 - roll_chances[name])
    #     reroll_profit[name] = reroll_result - type_data.prices[name] - lifeforce_price

    # # shows what to reroll when will lose at least 1c from rerolling, how to determine profit?
    # should_reroll = [name for name, profit in reroll_profit.items() if profit < -1]

    # # get weights for each option
    # roll_chances = dict(sorted(roll_chances.items(), key=lambda x: x[1], reverse=True))

    while True:
        lifeforce_cost = type_data.lifeforce_used / type_data.lifeforce * num_rolls

        # probability * expected return (price - cost)

        # probability of getting in x rolls = (1 - ((1 - (count / total_value)) ** num_rolls))
        # expected return = (price - min price - lifeforce) IF POSITIVE, else (- min price - lifeforce)
        #       will never sell if still at a loss for ev, so can't include price of item

        potential_ev = {
            name: (
                (1 - ((1 - (count / total_value)) ** num_rolls))
                * (type_data.prices[name] - type_data.min_price - lifeforce_cost)
                if (type_data.prices[name] - type_data.min_price - lifeforce_cost) >= 0
                else (1 - ((1 - (count / total_value)) ** num_rolls))
                * (-type_data.min_price - lifeforce_cost)
            )
            for name, count in type_data.weights.items()
        }

        # potential_ev = {}

        # for name, weight in type_data.weights.items():
        #     roll_names = set(type_data.weights.keys())
        #     name = roll_names.intersection(name.replace("'s", "").split())
        #     if (type_data.api_data[name] - type_data.min_price - lifeforce_cost) >= 0:
        #         potential_ev[name] = (
        #             1 - ((1 - (weight / total_value)) ** num_rolls)
        #         ) * (type_data.api_data[name] - type_data.min_price - lifeforce_cost)
        #     else:
        #         (1 - ((1 - (weight / total_value)) ** num_rolls)) * (
        #             -type_data.min_price - lifeforce_cost
        #         )

        total_ev = sum(potential_ev.values())

        # if the total expected value is more than the maxmimum expected value,
        # set current ev to maximum and check ev for rolling an additional time
        if total_ev > max_ev:
            expected_value = potential_ev
            max_ev = total_ev
            num_rolls += 1

        else:
            num_rolls -= 1  # the final roll didn't have better ev
            break

    # valuable items have positive ev
    valuable = {name: value for name, value in expected_value.items() if value >= 0}
    valuable = dict(sorted(valuable.items(), key=lambda x: x[1], reverse=True))

    type_data.set_expected_value(expected_value)
    type_data.set_valuable(valuable)

    type_data.set_avg_rolls(num_rolls)


if __name__ == "__main__":
    start_harvest_main()
