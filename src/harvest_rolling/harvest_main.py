#


from typing import List
from api_data import API_Data
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "harvest_rolling.txt")


class Type_Data:
    def __init__(
        self,
        type,
        rolls,
        prices,
        lifeforce_name,
        lifeforce_type,
        lifeforce_used,
        invalid,
    ):
        self.type = type
        self.rolls = rolls
        self.lifeforce_type = lifeforce_type
        self.lifeforce_name = lifeforce_name
        self.lifeforce_used = lifeforce_used
        self.invalid = invalid

        self.set_prices(prices)

    def set_valuable(self, valuable):
        self.valuable = valuable

    def set_expected_value(self, expected_value):
        self.expected_value = expected_value

        # avg expected value
        self.profit_per_roll = sum(self.expected_value.values()) / len(
            self.expected_value
        )

        self.rolls_per_div = API_Data.divine / self.min_price
        self.profit_per_div = self.profit_per_roll * self.rolls_per_div

    def set_prices(self, prices):
        roll_names = set(self.rolls.keys())
        self.prices = {}
        self.min_price = float("inf")

        for price_data in prices:
            name = price_data.get("name", price_data.get("currencyTypeName"))
            if any(invalid_name in name for invalid_name in self.invalid):
                continue

            name = roll_names.intersection(name.replace("'s", "").split())
            if name:
                price = price_data.get("chaosValue", price_data.get("chaosEquivalent"))
                self.prices[name.pop()] = price
                if price < self.min_price:
                    self.min_price = price

    def set_avg_rolls(self, rolls):
        self.avg_rolls = rolls


def start_harvest_main():
    harvest_rerolls = [
        Type_Data(
            "Fossil",
            {
                "Aberrant": 1,
                "Aetheric": 1,
                "Bound": 1,
                "Corroded": 1,
                "Deft": 1,
                "Dense": 1,
                "Frigid": 1,
                "Fundamental": 1,
                "Gilded": 1,
                "Jagged": 1,
                "Lucent": 1,
                "Metallic": 1,
                "Perfect": 1,
                "Prismatic": 1,
                "Pristine": 1,
                "Sanctified": 1,
                "Scorched": 1,
                "Serrated": 1,
                "Shuddering": 1,
            },
            API_Data.fossil_data,
            "Red",
            API_Data.lifeforce_red,
            30,
            ["Bloodstained", "Faceted", "Fractured", "Glyphic", "Hollow", "Tangled"],
        ),
        Type_Data(
            "Oil",
            {
                "Golden": 0,
                "Silver": 0,
                "Opalescent": 0,
                "Black": 2,
                "Crimson": 4,
                "Violet": 8,
                "Azure": 10,
                "Indigo": 5,
                "Teal": 20,
                "Verdant": 31,
                "Amber": 49,
                "Clear": 70,
                "Sepia": 55,
            },
            API_Data.oil_data,
            "Yellow",
            API_Data.lifeforce_yellow,
            30,
            ["Tainted", "Reflective"],
        ),
        Type_Data(
            "Catalyst",
            {
                "Intrinsic": 485,
                "Imbued": 301,
                "Noxious": 297,
                "Turbulent": 296,
                "Abrasive": 292,
                "Prismatic": 91,
                "Fertile": 88,
                "Tempering": 83,
                "Accelerating": 35,
                "Unstable": 32,
            },
            API_Data.catalyst_data,
            "Yellow",
            API_Data.lifeforce_yellow,
            30,
            ["Tainted"],
        ),
        Type_Data(
            "Essence",
            {
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
            API_Data.essence_data,
            "Blue",
            API_Data.lifeforce_blue,
            30,
            [
                "Horror",
                "Delirium",
                "Insanity",
                "Hysteria",
                "Shrieking",
                "Muttering",
                "Screaming",
                "Wailing",
                "Weeping",
                "Whispering",
                "Remnant",
            ],
        ),
        Type_Data(
            "Timeless Splinter",
            {
                "Eternal": 1,
                "Karui": 1,
                "Maraketh": 1,
                "Templar": 1,
                "Vaal": 1,
            },
            API_Data.timeless_splinter_data,
            "Blue",
            API_Data.lifeforce_blue,
            4,
            [],
        ),
        Type_Data(
            "Timeless Emblem",
            {
                "Eternal": 1,
                "Karui": 1,
                "Maraketh": 1,
                "Templar": 1,
                "Vaal": 1,
            },
            API_Data.timeless_emblem_data,
            "Blue",
            API_Data.lifeforce_blue,
            400,
            ["Unrelenting"],
        ),
        Type_Data(
            "Breach Splinter",
            {
                "Chayula": 1,
                "Esh": 1,
                "Tul": 1,
                "Uul-Netol": 1,
                "Xoph": 1,
            },
            API_Data.breach_splinter_data,
            "Red",
            API_Data.lifeforce_red,
            4,
            [],
        ),
        Type_Data(
            "Breach Stone",
            {
                "Chayula": 1,
                "Esh": 1,
                "Tul": 1,
                "Uul-Netol": 1,
                "Xoph": 1,
            },
            API_Data.breach_stone_data,
            "Red",
            API_Data.lifeforce_red,
            400,
            ["Flawless"],
        ),
        Type_Data(
            "Delirium Orb",
            {
                "Armoursmith": 608,
                "Jeweller": 584,
                "Blacksmith": 546,
                "Fine": 542,
                "Diviner": 344,
                "Whispering": 313,
                "Foreboding": 304,
                # "Imperial": 287,
                "Cartographer": 186,
                "Abyssal": 172,
                "Blighted": 167,
                "Timeless": 164,
                "Thaumaturge": 161,
                "Skittering": 156,
                "Fossilised": 150,
                # "Amorphous": 149,
                "Fragmented": 138,
                "Singular": 132,
                "Obscured": 83,
            },
            API_Data.delirium_orb_data,
            "Blue",
            API_Data.lifeforce_blue,
            30,
            [],
        ),
        Type_Data(
            "Shaper Fragment",
            {
                "Hydra": 1,
                "Chimera": 1,
                "Minotaur": 1,
                "Phoenix": 1,
            },
            API_Data.fragment_data,
            "Red",
            API_Data.lifeforce_red,
            500,
            [],
        ),
        Type_Data(
            "Elder Fragment",
            {
                "Purification": 1,
                "Constriction": 1,
                "Eradication": 1,
                "Enslavement": 1,
            },
            API_Data.fragment_data,
            "Blue",
            API_Data.lifeforce_blue,
            500,
            [],
        ),
        Type_Data(
            "Conqueror Fragment",
            {
                "Al-Hezmin": 1,
                "Baran": 1,
                "Drox": 1,
                "Veritania": 1,
            },
            API_Data.fragment_data,
            "Yellow",
            API_Data.lifeforce_yellow,
            500,
            [],
        ),
        Type_Data(
            "Sacrifice Fragment",
            {
                "Dusk": 1,
                "Noon": 1,
                "Dawn": 1,
                "Midnight": 1,
            },
            API_Data.fragment_data,
            "Blue",
            API_Data.lifeforce_blue,
            500,
            [],
        ),
        Type_Data(
            "Mortal Fragment",
            {
                "Grief": 1,
                "Ignorance": 1,
                "Hope": 1,
                "Rage": 1,
            },
            API_Data.fragment_data,
            "Blue",
            API_Data.lifeforce_blue,
            500,
            [],
        ),
        Type_Data(
            "Uber Elder Fragment",
            {
                "Knowledge": 1,
                "Shape": 1,
                "Emptiness": 1,
                "Terror": 1,
            },
            API_Data.fragment_data,
            "Yellow",
            API_Data.lifeforce_yellow,
            800,
            [],
        ),
    ]

    for reroll_type in harvest_rerolls:
        calc_prices(reroll_type)

    harvest_rerolls = sorted(
        harvest_rerolls, key=lambda x: x.profit_per_div, reverse=True
    )

    write_results(harvest_rerolls)


def write_results(reroll_data: List[Type_Data]):
    with open(RESULTS_FILE, "w") as file:
        pass

    with open(RESULTS_FILE, "a") as file:
        file.write("\n---------- Lifeforce per Chaos ----------\n\n")

        file.write(
            f"{'Yellow:':8} {round(API_Data.lifeforce_yellow - 5)} per chaos | {round((API_Data.lifeforce_yellow - 5) * API_Data.divine)} per div\n"
        )
        file.write(
            f"{'Blue:':8} {round(API_Data.lifeforce_blue - 5)} per chaos | {round((API_Data.lifeforce_blue - 5) * API_Data.divine)} per div\n"
        )
        file.write(
            f"{'Red:':8} {round(API_Data.lifeforce_red - 5)} per chaos | {round((API_Data.lifeforce_red - 5) * API_Data.divine)} per div \n\n"
        )

        for reroll in reroll_data:
            if reroll.profit_per_div > 0:
                file.write(f"---------- {reroll.type} ----------\n\n")

                # file.write(
                #     f"Avg Profit per Reroll: {round(reroll.profit_per_roll, 5)}\n"
                # )
                file.write(
                    f"Avg Profit per Divine (x{round(reroll.rolls_per_div)}): {round(reroll.profit_per_roll * (API_Data.divine / reroll.min_price), 2)}\n\n"
                )
                file.write(f"Lifeforce: {reroll.lifeforce_name}\n")
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
def calc_prices(type_data: Type_Data):

    # using roll data, find percentages
    total_value = sum(type_data.rolls.values())

    # number of harvest rolls
    num_rolls = 1

    max_ev = float("-inf")
    expected_value = {}

    while True:
        lifeforce_cost = type_data.lifeforce_used / type_data.lifeforce_type * num_rolls

        # probability * expected return (price - cost)
        potential_ev = {
            name: (1 - ((1 - (count / total_value)) ** num_rolls))
            * (type_data.prices[name] - type_data.min_price - lifeforce_cost)
            for name, count in type_data.rolls.items()
        }
        total_ev = sum(potential_ev.values())

        if total_ev > max_ev:
            expected_value = potential_ev
            max_ev = total_ev
            num_rolls += 1

        else:
            break

    valuable = {name: value for name, value in expected_value.items() if value > 0}

    valuable = dict(sorted(valuable.items(), key=lambda x: x[1], reverse=True))

    type_data.set_expected_value(expected_value)
    type_data.set_valuable(valuable)

    # last roll didn't have better ev
    type_data.set_avg_rolls(num_rolls - 1)
