#

from backend.scripts.api_data import API_Data
from backend.scripts.keys import Keys
from backend.scripts.harvest_rolling.harvest_rolls import TypeData, get_harvest_rolls


RESULTS_FILE = "backend/results/harvest_rolling.txt"


class HarvestRollingData:
    def __init__(self, keys: Keys):
        api_data = API_Data().all_data

        self.divine_cost = api_data[keys.DIVINE][keys.CHAOS]
        self.yellow_lifeforce_per_chaos = (
            1 / api_data[keys.YELLOW_LIFEFORCE][keys.CHAOS]
        )
        self.blue_lifeforce_per_chaos = 1 / api_data[keys.BLUE_LIFEFORCE][keys.CHAOS]
        self.red_lifeforce_per_chaos = 1 / api_data[keys.RED_LIFEFORCE][keys.CHAOS]

        self.harvest_rerolls = None


def start_harvest_main():
    keys = Keys()
    harvest_data = HarvestRollingData(keys)
    harvest_rerolls = get_harvest_rolls(keys)

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
            f"{'Yellow:':8} {round(harvest_data.yellow_lifeforce_per_chaos)} per chaos | {round((harvest_data.yellow_lifeforce_per_chaos) * harvest_data.divine_cost)} per div\n"
        )
        file.write(
            f"{'Blue:':8} {round(harvest_data.blue_lifeforce_per_chaos)} per chaos | {round((harvest_data.blue_lifeforce_per_chaos) * harvest_data.divine_cost)} per div\n"
        )
        file.write(
            f"{'Red:':8} {round(harvest_data.red_lifeforce_per_chaos)} per chaos | {round((harvest_data.red_lifeforce_per_chaos) * harvest_data.divine_cost)} per div \n\n"
        )

        for reroll in harvest_data.harvest_rerolls:
            reroll: TypeData
            if reroll.profit_per_div > 0:
                file.write(f"---------- {reroll.name} ----------\n\n")

                # file.write(
                #     f"Avg Profit per Reroll: {round(reroll.total_ev, 5)}\n"
                # )

                file.write(
                    f"Avg Profit per Divine (x{round(reroll.rolls_per_div)}): {round(reroll.profit_per_div, 2)}c \n\n"
                )

                file.write(
                    f"Buying At: {round(reroll.buy_in, 2)}c each | {round(harvest_data.divine_cost/reroll.buy_in)} per div\n"
                )
                file.write(f"Avg Rolls: {round(reroll.avg_rolls)}\n")
                file.write(f"Lifeforce: {reroll.lifeforce_name}\n\n")
                # for name, price in type_data.stop_on.items():
                #     file.write(f"{name}: {round(type_data.prices[name])}\n")

                sell_names = ", ".join(reroll.stop_on)
                file.write(f"Sell: {sell_names}\n")

                buy_names = ", ".join(reroll.roll_on)
                file.write(f"Buy: {buy_names}\n\n")


# find rolls w/ higher price that potential prices of other rolls
def calc_prices(harvest_data: HarvestRollingData, type_data: TypeData):

    total_weight = sum(type_data.weights.values())

    lifeforce_cost_per_roll = type_data.lifeforce_used / type_data.lifeforce_per_chaos

    expected_values = {}

    for current_name, current_weight in type_data.weights.items():
        remaining_weight = total_weight - current_weight
        current_price = type_data.prices[current_name]
        current_ev = 0

        for temp_name, temp_weight in type_data.weights.items():
            if temp_name == current_name:
                continue

            probability = temp_weight / remaining_weight
            current_ev += probability * type_data.prices[temp_name]

        generic_ev = current_ev - current_price

        expected_values[current_name] = generic_ev

    def _calc_ev(names, type_data: TypeData, stop_weight):
        total_ev = 0

        for name in names:
            weight = type_data.weights[name]
            price = type_data.prices[name]

            prob = weight / stop_weight

            total_ev += prob * price

        return total_ev

    expected_values = dict(sorted(expected_values.items(), key=lambda item: item[1]))

    roll_weight = 0
    stop_weight = total_weight
    roll_on = []
    stop_on = [name for name in expected_values.keys()]
    max_total_ev = float("-inf")
    max_roll_on = []
    max_stop_on = []
    max_avg_rolls = -1
    max_rolls_per_div = -1
    max_profit_per_div = -1

    while len(stop_on) > 1:
        name = stop_on.pop()
        roll_on.append(name)

        weight = type_data.weights[name]

        roll_weight += weight
        stop_weight -= weight

        avg_rolls = total_weight / stop_weight

        total_ev = _calc_ev(stop_on, type_data, stop_weight)

        cost_per_roll = type_data.buy_in + avg_rolls * lifeforce_cost_per_roll
        total_ev -= cost_per_roll
        rolls_per_div = harvest_data.divine_cost / cost_per_roll
        profit_per_div = total_ev * rolls_per_div

        if profit_per_div > max_profit_per_div:
            max_total_ev = total_ev
            max_avg_rolls = avg_rolls
            max_roll_on = roll_on.copy()
            max_stop_on = stop_on.copy()
            max_rolls_per_div = rolls_per_div
            max_profit_per_div = profit_per_div

    type_data.stop_on = max_stop_on
    type_data.roll_on = max_roll_on

    type_data.rolls_per_div = max_rolls_per_div
    type_data.profit_per_div = max_profit_per_div

    type_data.avg_rolls = max_avg_rolls

    type_data.total_ev = max_total_ev


if __name__ == "__main__":

    start_harvest_main()
