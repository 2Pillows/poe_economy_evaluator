# chaos_res_crafting_main

from api_data import API_Data

import os


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "chaos_res_crafting.txt")

# Harvest crafting for T1 Chaos Res is 1/7
# Each reforge chaos is 70 yellow lifeforce
yellow_needed = 700

# average rolls

# deafening envy and getting t3+ res w/ life or open prefix
AVG_ENVY_RES_LIFE = 6


def start_chaos_res_crafting():
    harvest_cost = yellow_needed / API_Data.lifeforce_yellow
    API_Data.deafening_envy = API_Data.deafening_envy
    yellow_equiv = yellow_needed / API_Data.deafening_envy

    # find cost of stygian crafting
    stygian_cost = (
        API_Data.stygian_vise
        + (min(harvest_cost, API_Data.deafening_envy) * AVG_ENVY_RES_LIFE)
        + (4 * API_Data.catalyst_fertile)
        + API_Data.scour
        + API_Data.alch
    )

    write_results(harvest_cost, yellow_equiv, stygian_cost)


def write_results(harvest_cost, yellow_equiv, stygian_cost):
    # clear file
    with open(RESULTS_FILE, "w") as file:
        pass

    # write data to file
    with open(RESULTS_FILE, "a", encoding="utf-8") as file:
        file.write("\n---------- Rolling Cost ----------\n\n")
        file.write(
            f"Harvest Reforge Chaos (~700 Yellow): {round(harvest_cost)} chaos total \n\tBuy: {round(API_Data.lifeforce_yellow)} per chaos | {round(API_Data.divine * API_Data.lifeforce_yellow):,} per div\n"
        )
        if yellow_equiv > 0:
            file.write(
                f"\tEquiv to Essence: {round(yellow_equiv)} per chaos | {round(yellow_equiv * API_Data.divine):,} per div\n\n"
            )
        file.write(
            f"Deafening Envy: {round(API_Data.deafening_envy)} chaos | {round(API_Data.divine / API_Data.deafening_envy, 2)} per div\n"
        )

        file.write("\n---------- Crafting Cost ----------\n\n")
        file.write(
            f"Stygian Vise: {round(stygian_cost)}c avg total \n\tiLvl 86 Base: {round(API_Data.stygian_vise)}c \n\t4x Fertile Catalyst: {round(4 * API_Data.catalyst_fertile)} chaos total | {round(API_Data.catalyst_fertile)} chaos per or {round(API_Data.divine / API_Data.catalyst_fertile, 2)} per div \n"
        )
        if harvest_cost < API_Data.deafening_envy:
            file.write(
                f"\t {AVG_ENVY_RES_LIFE * yellow_needed}x Yellow Juice: {harvest_cost * AVG_ENVY_RES_LIFE} chaos total"
            )
        else:
            file.write(
                f"\t{AVG_ENVY_RES_LIFE}x Deafening Envy: {API_Data.deafening_envy * AVG_ENVY_RES_LIFE} chaos total"
            )
