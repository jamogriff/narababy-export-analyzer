from dataclasses import dataclass
from .models.baby import Baby
from .models.caregiver import Caregiver
from .models.milk_feed import MilkFeed
from .models.diaper_change import DiaperChange
from .models.pump import Pump


@dataclass
class ModelResults:
    babies: list[Baby]
    caregivers: list[Caregiver]
    bottles: list[MilkFeed]
    diapers: list[DiaperChange]
    pumps: list[Pump]
