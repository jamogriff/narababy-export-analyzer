from abc import abstractmethod, ABC
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..models.base import Base


class AbstractRepository(ABC):

    def __init__(self, session: Session, model: Base):
        self.session = session
        self.model = model

    def count(self) -> int:
        with self.session as session:
            stmt = select(func.count()).select_from(self.model)
            count = session.execute(stmt).scalar_one()

        return count
