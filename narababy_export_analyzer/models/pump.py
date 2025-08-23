from __future__ import annotations
import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..dtos.narababy_pump_row import NarababyPumpRow
from ..utils import datetime_utils as date
from .caregiver import Caregiver
from .base import Base


class Pump(Base):
    """An occurrance of pumping milk."""

    __tablename__ = "pump"

    id: Mapped[int] = mapped_column(primary_key=True)
    caregiver_id: Mapped[int] = mapped_column(ForeignKey("caregiver.id"))
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime)

    caregiver: Mapped["Caregiver"] = relationship(back_populates="pumps")

    def __init__(self, caregiver: Caregiver, timestamp: datetime.datetime):
        self.caregiver = caregiver
        self.timestamp = timestamp

    @classmethod
    def from_narababy_pump_row(
        cls, narababy_row: NarababyPumpRow, caregiver: Caregiver
    ) -> Pump:
        return cls(
            caregiver,
            date.create_date_from_narababy_event(
                narababy_row.timestamp, narababy_row.timezone
            ),
        )
