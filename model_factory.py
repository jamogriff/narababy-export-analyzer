from .parse_results import ParseResults
from .dtos.narababy_event_row import NarababyEventRow
from .dtos.narababy_bottle_feed_row import NarababyBottleFeedRow
from .dtos.narababy_pump_row import NarababyPumpRow
from .dtos.narababy_diaper_row import NarababyDiaperRow
from .models.milk_feed import MilkFeed
from .models.diaper_change import DiaperChange
from .models.pump import Pump
from .models.caregiver import Caregiver
from .models.baby import Baby
from .model_results import ModelResults


class ModelFactory:
    """Class to create models with refined data from ParseResults"""

    def __init__(self, parse_results: ParseResults):
        self.data: list[NarababyEventRow] = parse_results.data

    def make(self) -> ModelResults:
        caregivers: list[Caregiver] = []
        babies: list[Baby] = []
        feeds: list[MilkFeed] = []
        diaper_changes: list[DiaperChange] = []
        pumps: list[Pump] = []
        for event in self.data:
            # Since we are processing flat CSV data that contains
            # many-to-one relations, extract the baby and caregiver
            # models that own subsequent events
            baby = self._get_baby(event.baby, babies)

            if not baby:
                baby = Baby(event.baby)
                babies.append(baby)

            caregiver = self._get_caregiver(event.caregiver, caregivers)

            if not caregiver:
                caregiver = Caregiver(event.caregiver)
                caregivers.append(caregiver)

            # Now process the event specific data and pass owning
            # relation instances in
            if isinstance(event, NarababyBottleFeedRow):
                feeds.append(
                    MilkFeed.from_narababy_bottle_feed_row(event, baby, caregiver)
                )
            elif isinstance(event, NarababyDiaperRow):
                diaper_changes.append(
                    DiaperChange.from_narababy_diaper_row(event, baby, caregiver)
                )
            elif isinstance(event, NarababyPumpRow):
                pumps.append(Pump.from_narababy_pump_row(event, caregiver))

        return ModelResults(babies, caregivers, feeds, diaper_changes, pumps)

    def _get_caregiver(
        self, name: str, caregivers: list[Caregiver]
    ) -> Caregiver | None:
        return next((c for c in caregivers if c.name == name), None)

    def _get_baby(self, name: str, babies: list[Baby]) -> Baby | None:
        return next((b for b in babies if b.name == name), None)
