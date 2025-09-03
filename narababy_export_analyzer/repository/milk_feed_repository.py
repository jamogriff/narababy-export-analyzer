from sqlalchemy.orm import Session
from .abstract_repository import AbstractRepository
from ..models.milk_feed import MilkFeed


class MilkFeedRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__(session, MilkFeed)

