from dataclasses import dataclass
from .dtos.narababy_event_row import NarababyEventRow


@dataclass
class ParseResults:
    data: list[NarababyEventRow]
    rows_processed: int
    time_elapsed: float
