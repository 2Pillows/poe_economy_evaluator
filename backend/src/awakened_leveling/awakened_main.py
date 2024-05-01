# awakened_main.py

from backend.src.api_data import API_Data, Singleton
from dataclasses import dataclass

MIN_PROFIT = 10
RESULTS_FILE = "backend/results/awakened_leveling.txt"


@dataclass
class AwakenedLevelingData(metaclass=Singleton):
    divine: int = None
    wild_brambleback: int = None
    gemcutter: int = None
    gem_margins: dict = None

    gem_data: list = None

    def set_api_data(self):
        api_data = API_Data()
        self.divine = api_data.divine
        self.wild_brambleback = api_data.wild_brambleback
        self.gemcutter = api_data.gemcutter
        self.gem_data = api_data.gem_data

    def set_results(self, gem_margins):
        self.gem_margins = gem_margins


def start_awakened_main():
    leveling_data = AwakenedLevelingData()
    leveling_data.set_api_data()

    gem_levels = sort_gem_data(leveling_data)

    gem_margins = calculate_gem_margins(leveling_data, gem_levels)

    leveling_data.set_results(gem_margins)

    write_to_file(leveling_data)


def sort_gem_data(leveling_data: AwakenedLevelingData):
    sorted_gems = {}

    for gem in leveling_data.gem_data:
        gem_name = gem.get("name")

        if not gem_name or "Awakened" not in gem_name:
            continue

        if any(keyword in gem_name for keyword in ["Empower", "Enhance", "Enlighten"]):
            continue

        gem_variant = gem.get("variant")
        if gem_variant and "c" in gem_variant:
            continue

        gem_level = gem.get("gemLevel")
        gem_chaos = gem.get("chaosValue")

        sorted_gems.setdefault(gem_name, {}).update({gem_level: gem_chaos})

    return sorted_gems


def calculate_gem_margins(leveling_data: AwakenedLevelingData, gem_levels):
    gem_margins = {}

    for name, prices in gem_levels.items():
        if 5 in prices and 1 in prices:
            profit = (
                prices[5]
                - prices[1]
                - (4 * leveling_data.wild_brambleback)
                - (20 * leveling_data.gemcutter)
            )
            gem_margins[name] = {"profit": profit, "buy": prices[1], "sell": prices[5]}

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
            if profit <= MIN_PROFIT:
                continue
            formatted_line = f"{name:50} | \t {round(profit):>5} | {round(profit/leveling_data.divine, 1):>5}  {round(buy):>8} | {round(buy/leveling_data.divine, 1):>5}  {round(sell):>8} | {round(sell/leveling_data.divine, 1):>5}"
            file.write(formatted_line + "\n")
        file.write(
            f"{'':50} | {'':3} chaos | {'div':>5} {'':3} chaos | {'div':>5} {'':3} chaos | {'div':>5}"
        )


if __name__ == "__main__":
    start_awakened_main()
