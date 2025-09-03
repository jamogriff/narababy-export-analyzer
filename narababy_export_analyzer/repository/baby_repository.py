from sqlalchemy.orm import Session
from .abstract_repository import AbstractRepository
from ..models.baby import Baby


class BabyRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__(session, Baby)

