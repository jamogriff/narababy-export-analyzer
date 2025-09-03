from sqlalchemy.orm import Session
from .abstract_repository import AbstractRepository
from ..models.caregiver import Caregiver


class CaregiverRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__(session, Caregiver)

