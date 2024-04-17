# sanctum_main.py

from api_data import API_Data

import os


LEAGUE_NAME = "Affliction"
NAME_KEY = "name"
COUNT_KEY = "count"
CHAOS_KEY = "chaos_equiv"
MIN_CHAOS = 10

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "sanctum_rewards.txt")
REWARD_FILE = os.path.join(CUR_DIR, "reward_data.txt")


def start_sanctum_main():
    reward_data = get_reward_data(REWARD_FILE)

    currency_prices = {
        item["currencyTypeName"]: item["chaosEquivalent"]
        for item in API_Data.currency_data
    }

    all_rewards = calculate_chaos(reward_data, currency_prices)

    good_rewards = [
        reward_data
        for reward_data in all_rewards
        if any(chaos > MIN_CHAOS for chaos in reward_data[CHAOS_KEY])
    ]

    sorted_rewards = sorted(all_rewards, key=lambda x: x[CHAOS_KEY][-1], reverse=True)

    write_to_file(sorted_rewards)
    # os.system(f"start {RESULTS_FILE}")


def get_reward_data(file):
    with open(file, "r") as file:
        data = []

        current_reward = {NAME_KEY: [], COUNT_KEY: []}

        for line in file:
            line = line.strip()  # Remove leading/trailing spaces

            if line:  # If the line is not empty
                if any(c.isalpha() for c in line):  # Check if it contains letters
                    current_reward[NAME_KEY].append(line)
                else:
                    current_reward[COUNT_KEY].append(int(line))
            else:
                if current_reward:
                    add_reward(current_reward, data)
                    current_reward = {NAME_KEY: [], COUNT_KEY: []}

        # Append any remaining data
        if current_reward[NAME_KEY] and current_reward[COUNT_KEY]:
            add_reward(current_reward, data)

    return data


def add_reward(reward_data, all_data):
    for reward_name in reward_data[NAME_KEY]:
        all_data.append({NAME_KEY: reward_name, COUNT_KEY: reward_data[COUNT_KEY]})


def calculate_chaos(reward_data, prices):
    all_chaos_equiv = []

    for reward_data in reward_data:
        name = reward_data[NAME_KEY]
        count = reward_data[COUNT_KEY]

        if name == "Chaos Orb":
            price = 1
        else:
            price = prices.get(name, None)

        if price is None:
            continue

        chaos_equiv = [round(amount * price) for amount in count]

        all_chaos_equiv.append({NAME_KEY: name, CHAOS_KEY: chaos_equiv})

    return all_chaos_equiv


def write_to_file(reward_data):
    with open(RESULTS_FILE, "w") as file:
        for reward in reward_data:
            name = reward[NAME_KEY]
            chaos_equivs = reward[CHAOS_KEY]
            formatted_line = f"{name:25} | {round(chaos_equivs[0])}, {round(chaos_equivs[1])}, {round(chaos_equivs[2])}"
            file.write(formatted_line + "\n")
