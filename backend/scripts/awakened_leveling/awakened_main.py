# awakened_main.py

from backend.scripts.api_data import API_Data
from backend.scripts.keys import Keys

MIN_PROFIT = 10
RESULTS_FILE = "backend/results/awakened_leveling.txt"


class AwakenedLevelingData:
    def __init__(self, keys: Keys):
        api_data = API_Data().all_data

        self.divine_cost = api_data[keys.DIVINE]["chaos"]
        self.wild_brambleback_cost = api_data[keys.WILD_BRAMBLEBACK]["chaos"]
        self.gemcutter_cost = api_data[keys.GEMCUTTER]["chaos"]
        self.min_lvl_gems = api_data[keys.MIN_LVL_AWAKENED_GEMS]
        self.max_lvl_gems = api_data[keys.MAX_LVL_AWAKENED_GEMS]
        self.max_lvl_max_qual_gems = api_data[keys.MAX_LVL_QUAL_AWAKENED_GEMS]

        self.level_cost = 4 * self.wild_brambleback_cost
        self.quality_cost = 20 * self.gemcutter_cost

        self.gem_margins = None


def start_awakened_main():
    keys = Keys()
    leveling_data = AwakenedLevelingData(keys)

    gem_margins = calculate_gem_margins(leveling_data, keys)

    leveling_data.gem_margins = gem_margins

    write_to_file(leveling_data)


def calculate_gem_margins(leveling_data: AwakenedLevelingData, keys: Keys):
    gem_margins = {}

    for name, min_gem in leveling_data.min_lvl_gems.items():
        max_gem = None

        # Max level and max quality gem
        if name in leveling_data.max_lvl_max_qual_gems:
            max_gem = leveling_data.max_lvl_max_qual_gems[name]
        # Max level wo/ quality. Need to add quality cost to chaos
        elif name in leveling_data.max_lvl_gems:
            max_gem = leveling_data.max_lvl_gems[name]
            max_gem += leveling_data.quality_cost
        else:
            continue

        min_price = min_gem[keys.CHAOS]
        max_price = max_gem[keys.CHAOS]

        profit = (
            max_price
            - min_price
            - leveling_data.level_cost
            - leveling_data.quality_cost
        )

        gem_margins[name] = {"profit": profit, "buy": min_price, "sell": max_price}

    sorted_gem_margins = dict(
        sorted(gem_margins.items(), key=lambda item: item[1]["profit"], reverse=True)
    )
    return sorted_gem_margins


def write_to_file(leveling_data: AwakenedLevelingData):
    with open(RESULTS_FILE, "w") as file:
        file.write(f"{'Gem Name':50} | {'':7} Profit {'':10} Buy {'':12} Sell\n")
        for name, margin in leveling_data.gem_margins.items():
            profit = margin["profit"]
            buy = margin["buy"]
            sell = margin["sell"]
            divine_price = leveling_data.divine_cost
            if profit <= MIN_PROFIT:
                continue
            formatted_line = f"{name:50} | \t {round(profit):>5} | {round(profit/divine_price, 1):>5}  {round(buy):>8} | {round(buy/divine_price, 1):>5}  {round(sell):>8} | {round(sell/divine_price, 1):>5}"
            file.write(formatted_line + "\n")
        file.write(
            f"{'':50} | {'':3} chaos | {'div':>5} {'':3} chaos | {'div':>5} {'':3} chaos | {'div':>5}"
        )


if __name__ == "__main__":
    start_awakened_main()
