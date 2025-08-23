from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Caregiver(Base):
    """An individual providing services to baby."""

    __tablename__ = "caregiver"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))  # TODO: how to add unique constraint
    feeds: Mapped[list["MilkFeed"]] = relationship(back_populates="caregiver")
    diaper_changes: Mapped[list["DiaperChange"]] = relationship(
        back_populates="caregiver"
    )
    pumps: Mapped[list["Pump"]] = relationship(back_populates="caregiver")

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other) -> bool:
        """This does not compare IDs for the sake of
        comparing during importing."""

        if not isinstance(other, Caregiver):
            return NotImplemented
        return self.name == other.name
