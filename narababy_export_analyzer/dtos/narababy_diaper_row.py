from .narababy_event_row import NarababyEventRow


class NarababyDiaperRow(NarababyEventRow):
    row_identifier: str = "Diaper"
    description: str | None

    def __str__(self) -> str:
        return f"{self.timestamp} by {self.caregiver}"

    def __repr__(self) -> str:
        return f"NarababyDiaperRow(description={self.description}, timestamp={self.timestamp}, timezone={self.timezone}, caregiver={self.caregiver})"

    @property
    def column_attribute_map(self) -> dict[int, str]:
        attribute_map = {16: "description"}
        shared_attributes = super().column_attribute_map
        return {**shared_attributes, **attribute_map}
