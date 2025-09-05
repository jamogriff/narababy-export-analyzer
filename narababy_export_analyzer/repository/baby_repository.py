from sqlalchemy import select, func
from sqlalchemy.orm import Session
from .abstract_repository import AbstractRepository
from ..models.baby import Baby
from ..models.milk_feed import MilkFeed
from ..models.diaper_change import DiaperChange


class BabyRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__(session, Baby)

    def find_all(self) -> list[Baby]:
        with self.session as session:
            return session.scalars(select(Baby)).all()

    def find_bottle_statistics(self, baby: Baby) -> tuple[str, int, float, float]:
        with self.session as session:
            stmt = (
                select(
                    self.model.name,
                    func.count(MilkFeed.id).label("total_bottles"),
                    func.round(func.sum(MilkFeed.volume) / 1000 / 3.785, 1).label(
                        "total_gallons"
                    ),
                    func.round(func.avg(MilkFeed.volume) / 29.574, 2).label(
                        "average_oz"
                    ),
                )
                .join(MilkFeed)
                .where(MilkFeed.baby == baby)
                .group_by(self.model.name)
            )
            return session.execute(stmt).first()

    def find_diaper_change_statistics(self, baby: Baby) -> tuple[str, int, int, int]:
        with self.session as session:
            stmt = (
                select(
                    self.model.name,
                    func.count(DiaperChange.id).label("total_diaper_changes"),
                    func.count(DiaperChange.id).filter(DiaperChange.is_poop == True).label("dirty_diapers"),
                    func.count(DiaperChange.id).filter(DiaperChange.is_pee == True).label("wet_diapers"),
                )
                .join(DiaperChange)
                .where(DiaperChange.baby == baby)
                .group_by(self.model.name)
            )
            return session.execute(stmt).first()
