from __future__ import annotations
import datetime
from sqlalchemy import Enum, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..dtos.narababy_bottle_feed_row import NarababyBottleFeedRow
from .caregiver import Caregiver
from .baby import Baby
from ..utils import datetime_utils as date
from ..utils import volume_utils as vol
from .base import Base


class MilkFeed(Base):
    """An event where a baby consumed milk."""

    __tablename__ = "feed"

    id: Mapped[int] = mapped_column(primary_key=True)
    baby_id: Mapped[int] = mapped_column(ForeignKey("baby.id"))
    caregiver_id: Mapped[int] = mapped_column(ForeignKey("caregiver.id"))
    volume: Mapped[float] = mapped_column(Float)
    unit: Mapped[vol.VolumeUnit] = mapped_column(
        Enum(vol.VolumeUnit, name="volume_unit")
    )
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime)

    baby: Mapped["Baby"] = relationship(back_populates="feeds")
    caregiver: Mapped["Caregiver"] = relationship(back_populates="feeds")

    def __init__(
        self,
        baby: Baby,
        caregiver: Caregiver,
        volume: float,
        unit: vol.VolumeUnit,
        timestamp: datetime.datetime,
    ):
        self.baby = baby
        self.caregiver = caregiver
        self.volume = volume
        self.unit = unit
        self.timestamp = timestamp

    @classmethod
    def from_narababy_bottle_feed_row(
        cls, narababy_row: NarababyBottleFeedRow, baby: Baby, caregiver: Caregiver
    ) -> MilkFeed:
        return cls(
            baby,
            caregiver,
            narababy_row.get_total_metric_volume(),
            vol.VolumeUnit.MILLILITER,
            date.create_date_from_narababy_event(
                narababy_row.timestamp, narababy_row.timezone
            ),
        )
