from __future__ import annotations
from enum import Enum


class VolumeUnit(Enum):
    """Unit of volume (e.g. mL, OZ)."""

    MILLILITER = "ML"
    OUNCE = "FLOZ"

    @classmethod
    def try_from(cls, value: str) -> VolumeUnit | None:
        try:
            return cls(value)
        except ValueError:
            return None


def fluid_ounces_to_milliliters(ounces: float) -> float:
    return ounces * 29.5735


def milliliters_to_fluid_ounces(milliliters: float) -> float:
    return milliliters / 29.5735
