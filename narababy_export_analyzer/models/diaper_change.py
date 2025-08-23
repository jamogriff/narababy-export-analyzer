from __future__ import annotations
import datetime
from sqlalchemy import DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..dtos.narababy_diaper_row import NarababyDiaperRow
from ..utils import datetime_utils as date
from .caregiver import Caregiver
from .baby import Baby
from .base import Base


class DiaperChange(Base):
    """An occurrance of a baby soiling themselves and getting cleaned."""

    __tablename__ = "diaper_change"

    id: Mapped[int] = mapped_column(primary_key=True)
    baby_id: Mapped[int] = mapped_column(ForeignKey("baby.id"))
    caregiver_id: Mapped[int] = mapped_column(ForeignKey("caregiver.id"))
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime)
    is_poop: Mapped[bool] = mapped_column(Boolean)
    is_pee: Mapped[bool] = mapped_column(Boolean)

    baby: Mapped["Baby"] = relationship(back_populates="diaper_changes")
    caregiver: Mapped["Caregiver"] = relationship(back_populates="diaper_changes")

    def __init__(
        self,
        baby: Baby,
        caregiver: Caregiver,
        timestamp: datetime.datetime,
        is_poop: bool,
        is_pee: bool,
    ):
        self.baby = baby
        self.caregiver = caregiver
        self.timestamp = timestamp
        self.is_poop = is_poop
        self.is_pee = is_pee

    @classmethod
    def from_narababy_diaper_row(
        cls, narababy_row: NarababyDiaperRow, baby: Baby, caregiver: Caregiver
    ) -> DiaperChange:
        return cls(
            baby,
            caregiver,
            date.create_date_from_narababy_event(
                narababy_row.timestamp, narababy_row.timezone
            ),
            "Dirty" in narababy_row.description if narababy_row.description else False,
            "Wet" in narababy_row.description if narababy_row.description else False,
        )
