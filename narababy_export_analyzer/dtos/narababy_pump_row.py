from .narababy_event_row import NarababyEventRow


class NarababyPumpRow(NarababyEventRow):
    row_identifier: str = "Pump"

    def __str__(self) -> str:
        return f"{self.timestamp} by {self.caregiver}"

    def __repr__(self) -> str:
        return (
            f"NarababyPumpRow(timestamp={self.timestamp}, caregiver={self.caregiver})"
        )

    @property
    def column_attribute_map(self) -> dict[int, str]:
        return super().column_attribute_map
