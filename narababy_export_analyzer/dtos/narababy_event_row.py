from __future__ import annotations
from abc import ABC, abstractmethod


class NarababyEventRow(ABC):
    registry: dict[str, type["NarababyEventRow"]] = {}
    timestamp: str
    timezone: str
    caregiver: str
    baby: str
    note: str
    row_identifier: str  # Subclasses must define this

    SHARED_COLUMN_ATTRIBUTE_MAP: dict[int, str] = {
        1: "baby",
        2: "timestamp",
        4: "caregiver",
        6: "note",
        7: "timezone",
    }

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "row_identifier"):
            raise TypeError(
                f"{cls.__name__} must define a class attribute 'row_identifier'."
            )
        NarababyEventRow.registry[cls.row_identifier] = cls

    @property
    @abstractmethod
    def column_attribute_map(self) -> dict[int, str]:
        """Subclasses should define their own column attribute mappings
        and then merge them with the shared ones provided by
        super().column_attribute_map."""

        return self.SHARED_COLUMN_ATTRIBUTE_MAP

    def hydrate_from_row(self, csv_row: list[str]) -> None:
        """Hydrates attributes of a subclass from a CSV row using its column_attribute_map."""

        for column_index, attr in self.column_attribute_map.items():
            setattr(self, attr, csv_row[column_index])
