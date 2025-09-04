from sqlalchemy.orm import Session
from .abstract_repository import AbstractRepository
from ..models.caregiver import Caregiver
from ..models.milk_feed import MilkFeed


class CaregiverRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__(session, Caregiver)

    def get_feeds_by_caregivers(self) -> tuple[str, int]:
        with self.session as session:
            stmt = (
                select(self.model.name, func.count(MilkFeed.id))
                .join(MilkFeed)
                .group_by(self.model.name)
            )
            result = self.session.execute(stmt).all()

        return result
