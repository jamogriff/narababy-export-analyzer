from sqlalchemy.orm import Session
from .abstract_repository import AbstractRepository
from ..models.baby import Baby


class BabyRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__(session, Baby)

    def find_bottle_statistics(self, baby: Baby) -> list[tuple[str, int, float, float]]:
        with self.session as session:
            stmt = (
                select(
                    baby_repo.model.name,
                    func.count(bottle_repo.model.id).label("total_bottles"),
                    func.round(
                        func.sum(bottle_repo.model.volume) / 1000 / 3.785, 1
                    ).label("total_gallons"),
                    func.round(func.avg(bottle_repo.model.volume) / 29.574, 2).label(
                        "average_oz"
                    ),
                )
                .join(bottle_repo.model)
                .where(bottle_repo.model.baby == jack)
                .group_by(baby_repo.model.name)
            )
            return session.execute(stmt).first()
