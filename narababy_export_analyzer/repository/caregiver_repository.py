from sqlalchemy.orm import Session
from .abstract_repository import AbstractRepository
from ..models.baby import Baby
from ..models.caregiver import Caregiver
from ..models.milk_feed import MilkFeed
from ..models.diaper_change import DiaperChange
from ..models.pump import Pump


class CaregiverRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__(session, Caregiver)

    def get_feeds_by_caregivers(self, baby: Baby) -> list[tuple[str, int]]:
        with self.session as session:
            stmt = (
                select(self.model.name, func.count(MilkFeed.id).label("total_feeds"))
                .outerjoin(MilkFeed)
                .where(MilkFeed.baby == baby)
                .group_by(self.model.name)
            )
            return self.session.execute(stmt).all()

    def get_diaper_changes_by_caregivers(self, baby: Baby) -> list[tuple[str, int]]:
        with self.session as session:
            stmt = (
                select(
                    self.model.name,
                    func.count(DiaperChange.id).label("total_diaper_changes"),
                )
                .outerjoin(DiaperChange)
                .where(DiaperChange.baby == baby)
                .group_by(self.model.name)
            )
            return self.session.execute(stmt).all()

    def get_pumps_by_caregivers(self) -> list[tuple[str, int]]:
        with self.session as session:
            stmt = (
                select(self.model.name, func.count(Pump.id).label("total_pumps"))
                .outerjoin(Pump)
                .group_by(self.model.name)
            )
            return self.session.execute(stmt).all()
