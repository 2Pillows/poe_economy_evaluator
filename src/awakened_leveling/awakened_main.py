# awakened_main.py

import os

MIN_PROFIT = 10

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "awakened_leveling.txt")


def sort_gem_data(gem_data):
    sorted_gems = {}

    for gem in gem_data:
        gem_name = gem.get("name")

        # remove non-upgradable gems
        if "Awakened" not in gem_name:
            continue
        if "Empower" in gem_name or "Enhance" in gem_name or "Enlighten" in gem_name:
            continue

        # remove corrupted gems
        gem_variant = gem.get("variant")
        if "c" in gem_variant:
            continue

        gem_level = gem.get("gemLevel")
        gem_chaos = gem.get("chaosValue")
        if gem_name not in sorted_gems:
            sorted_gems[gem_name] = {}
        sorted_gems[gem_name][gem_level] = gem_chaos

    return sorted_gems


def write_to_file(gem_data, divine_chaos):
    with open(RESULTS_FILE, "w") as file:
        file.write(f"{'Gem Name':50} | {'':7} Profit {'':10} Buy {'':12} Sell\n")
        for name, profit in gem_data.items():
            if profit[0] <= MIN_PROFIT:
                continue
            formatted_line = f"{name:50} | \t {round(profit[0]):>5} | {round(profit[0]/divine_chaos, 1):>5}  {round(profit[1]):>8} | {round(profit[1]/divine_chaos, 1):>5}  {round(profit[2]):>8} | {round(profit[2]/divine_chaos, 1):>5}"
            file.write(formatted_line + "\n")
        file.write(
            f"{'':50} | {'':3} chaos | {'div':>5} {'':3} chaos | {'div':>5} {'':3} chaos | {'div':>5}"
        )


def start_awakened_main(GEM_DATA, BEAST_DATA, CURRENCY_DATA):
    gem_levels = sort_gem_data(GEM_DATA)

    divine_chaos = next(
        (
            item["chaosEquivalent"]
            for item in CURRENCY_DATA
            if "Divine Orb" in item["currencyTypeName"]
        ),
        None,
    )

    wild_brambleback = {
        beast.get("name"): beast
        for beast in BEAST_DATA
        if "Wild Brambleback" in beast.get("name")
    }["Wild Brambleback"]
    wild_brambleback_chaos = wild_brambleback.get("chaosValue")

    gemcutter_chaos = {
        currency_item.get("currencyTypeName"): currency_item.get("chaosEquivalent")
        for currency_item in CURRENCY_DATA
        if "Gemcutter's Prism" in currency_item.get("currencyTypeName")
    }["Gemcutter's Prism"]

    gem_margins = {
        name: [
            prices[5]
            - prices[1]
            - (4 * wild_brambleback_chaos)
            - (20 * gemcutter_chaos),
            prices[1],
            prices[5],
        ]
        for name, prices in gem_levels.items()
        if 5 in prices and 1 in prices
    }

    sorted_gem_margins = dict(
        sorted(gem_margins.items(), key=lambda item: item[1], reverse=True)
    )

    write_to_file(sorted_gem_margins, divine_chaos)
    # os.system(f"start {FILE_NAME}")
