# chaos_res_crafting_main

from backend.src.api_data import API_Data, Singleton
from dataclasses import dataclass

RESULTS_FILE = (
    "/workspaces/poe_economy_evaluator/backend/results/chaos_res_crafting.txt"
)

# Harvest crafting for T1 Chaos Res is 1/7
# Each reforge chaos is 70 yellow lifeforce
yellow_needed = 700

# average rolls

# deafening envy and getting t3+ res w/ life or open prefix
AVG_ENVY_RES_LIFE = 6


@dataclass
class ChaosResCraftingData(metaclass=Singleton):

    lifeforce_yellow: float = None
    deafening_envy: float = None
    stygian_base_cost: float = None
    divine: float = None
    catalyst_fertile: float = None
    harvest_cost: float = None
    yellow_equiv: float = None
    stygian_crafting_cost: float = None

    scour: float = None
    alch: float = None

    def set_api_data(self):
        api_data = API_Data()
        self.lifeforce_yellow = api_data.lifeforce_yellow
        self.deafening_envy = api_data.deafening_envy
        self.stygian_base_cost = api_data.stygian_vise
        self.divine = api_data.divine
        self.catalyst_fertile = api_data.catalyst_fertile
        self.scour = api_data.scour
        self.alch = api_data.alch

    def set_results(self, _harvest_cost, _yellow_equiv, _stygian_cost):
        self.harvest_cost = _harvest_cost
        self.yellow_equiv = _yellow_equiv
        self.stygian_crafting_cost = _stygian_cost


def start_chaos_res_crafting():
    crafting_data = ChaosResCraftingData()
    crafting_data.set_api_data()

    harvest_cost = yellow_needed / crafting_data.lifeforce_yellow
    yellow_equiv = yellow_needed / crafting_data.deafening_envy
    envy_equiv = crafting_data.deafening_envy / yellow_needed

    # find cost of stygian crafting
    stygian_cost = (
        crafting_data.stygian_base_cost
        + (min(harvest_cost, crafting_data.deafening_envy) * AVG_ENVY_RES_LIFE)
        + (4 * crafting_data.catalyst_fertile)
        + crafting_data.scour
        + crafting_data.alch
    )

    crafting_data.set_results(harvest_cost, yellow_equiv, stygian_cost)

    write_results(crafting_data)


def write_results(crafting_data: ChaosResCraftingData):
    # clear file
    with open(RESULTS_FILE, "w") as file:
        pass

    # write data to file
    with open(RESULTS_FILE, "a", encoding="utf-8") as file:
        file.write("\n---------- Rolling Cost ----------\n\n")
        file.write(
            f"Harvest Reforge Chaos (~700 Yellow): {round(crafting_data.harvest_cost)} chaos total \n\tBuy: {round(crafting_data.lifeforce_yellow)} per chaos | {round(crafting_data.divine * crafting_data.lifeforce_yellow):,} per div\n"
        )
        if crafting_data.yellow_equiv > 0:
            file.write(
                f"\tEquiv to Essence: {round(crafting_data.yellow_equiv)} per chaos | {round(crafting_data.yellow_equiv * crafting_data.divine):,} per div\n\n"
            )
        file.write(
            f"Deafening Envy: {round(crafting_data.deafening_envy)} chaos | {round(crafting_data.divine / crafting_data.deafening_envy, 2)} per div\n"
        )

        file.write("\n---------- Crafting Cost ----------\n\n")
        file.write(
            f"Stygian Vise: {round(crafting_data.stygian_crafting_cost)}c avg total \n\tiLvl 86 Base: {round(crafting_data.stygian_crafting_cost)}c \n\t4x Fertile Catalyst: {round(4 * crafting_data.catalyst_fertile)} chaos total | {round(crafting_data.catalyst_fertile)} chaos per or {round(crafting_data.divine / crafting_data.catalyst_fertile, 2)} per div \n"
        )
        if crafting_data.harvest_cost < crafting_data.deafening_envy:
            file.write(
                f"\t {round(AVG_ENVY_RES_LIFE * yellow_needed)}x Yellow Juice: {round(crafting_data.harvest_cost * AVG_ENVY_RES_LIFE)} chaos total"
            )
        else:
            file.write(
                f"\t{AVG_ENVY_RES_LIFE}x Deafening Envy: {round(crafting_data.deafening_envy * AVG_ENVY_RES_LIFE)} chaos total"
            )


if __name__ == "__main__":
    start_chaos_res_crafting()
