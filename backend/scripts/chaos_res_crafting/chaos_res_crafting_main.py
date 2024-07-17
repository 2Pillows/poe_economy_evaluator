# chaos_res_crafting_main

from backend.scripts.api_data import API_Data
from backend.scripts.keys import Keys

RESULTS_FILE = "backend/results/chaos_res_crafting.txt"


# average rolls
# harvest is 1/31 for same rolls,
AVG_HARVEST_RES_LIFE = 31

# Harvest crafting for T1 Chaos Res is 1/7
# Each reforge chaos is 100 yellow lifeforce
YELLOW_NEEDED = 7 * 100 * AVG_HARVEST_RES_LIFE

# deafening envy and getting t3+ res and (t3+ life or open prefix)
ENVY_NEEDED = 6


class ChaosResCraftingData:
    def __init__(self, keys: Keys):
        api_data = API_Data().all_data

        # ref objects used to intellisense
        self.yellow_lifeforce_per_chaos = (
            1 / api_data[keys.YELLOW_LIFEFORCE][keys.CHAOS]
        )
        self.deafening_envy_cost = api_data[keys.DEAFENING_ENVY][keys.CHAOS]
        self.stygian_base_cost = api_data[keys.STYGIAN_i86_BASE][keys.CHAOS]
        self.divine_cost = api_data[keys.DIVINE][keys.CHAOS]
        self.fertile_catalyst_cost = api_data[keys.FERTILE_CATALYST][keys.CHAOS]
        self.scour_cost = api_data[keys.SCOUR][keys.CHAOS]
        self.alch_cost = api_data[keys.ALCH][keys.CHAOS]

        self.harvest_crafting_cost = None
        self.deafening_crafting_cost = None
        self.yellow_equiv = None
        self.envy_equiv = None
        self.stygian_crafting_cost = None


def start_chaos_res_crafting():
    keys = Keys()
    crafting_data = ChaosResCraftingData(keys)

    harvest_crafting_cost = YELLOW_NEEDED / crafting_data.yellow_lifeforce_per_chaos
    deafening_crafting_cost = crafting_data.deafening_envy_cost * ENVY_NEEDED

    yellow_equiv = YELLOW_NEEDED / deafening_crafting_cost
    envy_equiv = deafening_crafting_cost / YELLOW_NEEDED

    # find cost of stygian crafting
    stygian_cost = (
        crafting_data.stygian_base_cost
        + min(harvest_crafting_cost, deafening_crafting_cost)
        + (4 * crafting_data.fertile_catalyst_cost)
        + crafting_data.scour_cost
        + crafting_data.alch_cost
    )

    crafting_data.harvest_crafting_cost = harvest_crafting_cost
    crafting_data.deafening_crafting_cost = deafening_crafting_cost
    crafting_data.yellow_equiv = yellow_equiv
    crafting_data.envy_equiv = envy_equiv
    crafting_data.stygian_crafting_cost = stygian_cost

    write_results(crafting_data)


def write_results(crafting_data: ChaosResCraftingData):
    # clear file
    with open(RESULTS_FILE, "w") as file:
        pass

    # write data to file
    with open(RESULTS_FILE, "a", encoding="utf-8") as file:
        file.write("\n---------- Rolling Cost ----------\n\n")

        file.write(
            f"Harvest Reforge Chaos (~{YELLOW_NEEDED} Yellow): {round(crafting_data.harvest_crafting_cost)} chaos total \n\tBuy: {round(crafting_data.yellow_lifeforce_per_chaos)} per chaos | {round(crafting_data.yellow_lifeforce_per_chaos * crafting_data.divine_cost):,} per div\n"
        )
        if crafting_data.yellow_equiv >= 1:
            file.write(
                f"\tEquiv to Essence: {round(crafting_data.yellow_equiv)} per chaos | {round(crafting_data.yellow_equiv * crafting_data.divine_cost):,} per div\n\n"
            )
        file.write(
            f"Essence Spamming (~{ENVY_NEEDED} Envy): {round(crafting_data.deafening_crafting_cost)} chaos total \n\tBuy: {round(crafting_data.deafening_envy_cost)} chaos | {round(crafting_data.divine_cost/crafting_data.deafening_envy_cost):,} per div\n"
        )
        if crafting_data.envy_equiv >= 1:
            file.write(
                f"\tEquiv to Lifeforce: {round(crafting_data.envy_equiv)} per chaos | {round(crafting_data.envy_equiv * crafting_data.divine_cost):,} per div\n\n"
            )

        file.write("\n---------- Crafting Cost ----------\n\n")
        file.write(
            f"Stygian Vise: {round(crafting_data.stygian_crafting_cost)}c avg total \n\tiLvl 86 Base: {round(crafting_data.stygian_base_cost)}c \n\t4x Fertile Catalyst: {round(4 * crafting_data.fertile_catalyst_cost)} chaos total | {round(crafting_data.fertile_catalyst_cost)} chaos per or {round(crafting_data.divine_cost / crafting_data.fertile_catalyst_cost, 2)} per div \n"
        )
        if crafting_data.harvest_crafting_cost < crafting_data.deafening_crafting_cost:
            file.write(
                f"\t {round(YELLOW_NEEDED)}x Yellow Juice: {round(crafting_data.harvest_crafting_cost)} chaos total"
            )
        else:
            file.write(
                f"\t{ENVY_NEEDED}x Deafening Envy: {round(crafting_data.deafening_crafting_cost)} chaos total"
            )


if __name__ == "__main__":
    start_chaos_res_crafting()
