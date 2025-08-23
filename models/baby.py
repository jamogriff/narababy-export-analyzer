from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Baby(Base):
    """An individual who cannot provide for themselves."""

    __tablename__ = "baby"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    feeds: Mapped[list["MilkFeed"]] = relationship(back_populates="baby")
    diaper_changes: Mapped[list["DiaperChange"]] = relationship(back_populates="baby")

    def __init__(self, name: str):
        self.name = name
