from sqlalchemy.orm import Session
from .abstract_repository import AbstractRepository
from ..models.diaper_change import DiaperChange


class DiaperChangeRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__(session, DiaperChange)
