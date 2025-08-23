from .narababy_event_row import NarababyEventRow
from ..utils import volume_utils as vol


class NarababyBottleFeedRow(NarababyEventRow):
    row_identifier: str = "Bottle Feed"
    breast_feed_volume: str
    breast_feed_unit: str
    formula_feed_volume: str
    formula_feed_unit: str
    volume: str
    unit: str

    def __str__(self) -> str:
        return f"{self.volume} {self.unit} at {self.timestamp} by {self.caregiver}"

    def __repr__(self) -> str:
        return f"NarababyBottleFeedRow(breast_feed_volume={self.breast_feed_volume} breast_feed_unit={self.breast_feed_unit} formula_feed_volume={self.formula_feed_volume} formula_feed_unit={self.formula_feed_unit} volume={self.volume}, unit={self.unit}, timestamp={self.timestamp}, caregiver={self.caregiver})"

    @property
    def column_attribute_map(self) -> dict[int, str]:
        attribute_map = {
            9: "breast_feed_volume",
            10: "breast_feed_unit",
            12: "formula_feed_volume",
            13: "formula_feed_unit",
            14: "volume",
            15: "unit",
        }

        return {**super().column_attribute_map, **attribute_map}

    def get_total_metric_volume(self) -> float:
        total_volume: float = 0.0
        if self.breast_feed_volume:
            if self.breast_feed_unit == vol.VolumeUnit.OUNCE.value:
                total_volume += vol.fluid_ounces_to_milliliters(
                    float(self.breast_feed_volume)
                )
            else:
                total_volume += float(self.breast_feed_volume)

        if self.formula_feed_volume:
            if self.formula_feed_unit == vol.VolumeUnit.OUNCE.value:
                total_volume += vol.fluid_ounces_to_milliliters(
                    float(self.formula_feed_volume)
                )
            else:
                total_volume += float(self.formula_feed_volume)

        if self.volume:
            if self.unit == vol.VolumeUnit.OUNCE.value:
                total_volume += vol.fluid_ounces_to_milliliters(float(self.volume))
            else:
                total_volume += float(self.volume)

        return total_volume
