from dataclasses import dataclass


@dataclass
class SharedState:
    divine: int = None
    wild_brambleback: int = None
    gemcutter: int = None
    gem_margins: dict = None
    gem_data: list = None
    lifeforce_yellow: float = None
    deafening_envy: float = None
    stygian_base_cost: float = None
    catalyst_fertile: float = None
    harvest_cost: float = None
    yellow_equiv: float = None
    stygian_crafting_cost: float = None
    scour: float = None
    alch: float = None

    # Class variable to hold the shared instance
    _shared_instance = None

    def __new__(cls):
        if cls._shared_instance is None:
            cls._shared_instance = super().__new__(cls)
        return cls._shared_instance


class AwakenedLevelingData:
    def __init__(self):
        self.shared_state = SharedState()

        self.divine = None
        self.lifeforce_yellow = None
        self.wild_brambleback = None
        self.gemcutter = None
        self.gem_margins = None
        self.gem_data = None

        self.gem_margins = None

    def __getattr__(self, attr):
        return getattr(SharedState, attr)

    def __setattr__(self, attr, value):
        if attr == "shared_state":
            super().__setattr__(attr, value)
        else:
            setattr(SharedState, attr, value)


class ChaosResCraftingData:
    def __init__(self):
        self.shared_state = SharedState()

        self.divine = None
        self.lifeforce_yellow = None
        self.wild_brambleback = None
        self.gemcutter = None
        self.gem_margins = None
        self.gem_data = None

        self.chaos_margins = None

    def __getattr__(self, attr):
        return getattr(SharedState, attr)

    def __setattr__(self, attr, value):
        if attr == "shared_state":
            super().__setattr__(attr, value)
        else:
            setattr(SharedState, attr, value)

    # Add similar properties for other attributes as needed


# Usage example:

awakened_data = AwakenedLevelingData()
chaos_res_data = ChaosResCraftingData()

# Setting a value in AwakenedLevelingData
awakened_data.divine = 150


# Getting the same value in ChaosResCraftingData
print(chaos_res_data.divine)  # Output: 100

# Setting a value in ChaosResCraftingData
chaos_res_data.lifeforce_yellow = 50

# Getting the same value in AwakenedLevelingData
print(awakened_data.lifeforce_yellow)  # Output: 50
