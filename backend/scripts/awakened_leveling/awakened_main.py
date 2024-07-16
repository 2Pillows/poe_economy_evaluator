# awakened_main.py

from backend.scripts.api_data import API_Data
from backend.scripts.keys import Keys

MIN_PROFIT = 10
RESULTS_FILE = "/workspaces/poe_economy_evaluator/backend/results/awakened_leveling.txt"


class AwakenedLevelingData:
    def __init__(self, keys: Keys):
        api_data = API_Data().all_data

        self.divine = api_data[keys.DIVINE]
        self.wild_brambleback = api_data[keys.WILD_BRAMBLEBACK]
        self.gemcutter = api_data[keys.GEMCUTTER]
        self.min_lvl_gems = api_data[keys.MIN_LVL_AWAKENED_GEMS]
        self.max_lvl_gems = api_data[keys.MAX_LVL_AWAKENED_GEMS]
        self.max_lvl_max_qual_gems = api_data[keys.MAX_LVL_QUAL_AWAKENED_GEMS]

        self.gem_margins = None
        self.level_cost = 4 * self.wild_brambleback[keys.CHAOS]
        self.quality_cost = 20 * self.gemcutter[keys.CHAOS]

    def __getattr__(self, attr):
        return API_Data().all_data[attr]

    def __setattr__(self, attr, value):
        if attr == "api_data":
            super().__setattr__(attr, value)
        else:
            API_Data().all_data[attr] = value


def start_awakened_main():
    keys = Keys()
    leveling_data = AwakenedLevelingData(keys)

    gem_margins = calculate_gem_margins(leveling_data, keys)

    leveling_data.gem_margins = gem_margins

    write_to_file(leveling_data, keys)


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
            max_gem[keys.CHAOS] += leveling_data.quality_cost
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


def write_to_file(leveling_data: AwakenedLevelingData, keys: Keys):
    with open(RESULTS_FILE, "w") as file:
        file.write(f"{'Gem Name':50} | {'':7} Profit {'':10} Buy {'':12} Sell\n")
        for name, margin in leveling_data.gem_margins.items():
            profit = margin["profit"]
            buy = margin["buy"]
            sell = margin["sell"]
            divine_price = leveling_data.divine[keys.CHAOS]
            if profit <= MIN_PROFIT:
                continue
            formatted_line = f"{name:50} | \t {round(profit):>5} | {round(profit/divine_price, 1):>5}  {round(buy):>8} | {round(buy/divine_price, 1):>5}  {round(sell):>8} | {round(sell/divine_price, 1):>5}"
            file.write(formatted_line + "\n")
        file.write(
            f"{'':50} | {'':3} chaos | {'div':>5} {'':3} chaos | {'div':>5} {'':3} chaos | {'div':>5}"
        )


if __name__ == "__main__":
    start_awakened_main()
