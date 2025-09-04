from sqlalchemy.orm import Session
from .model_results import ModelResults
from .repository.baby_repository import BabyRepository
from .repository.caregiver_repository import CaregiverRepository
from .repository.diaper_change_repository import DiaperChangeRepository
from .repository.milk_feed_repository import MilkFeedRepository
from .repository.pump_repository import PumpRepository
from .model_import_error import ModelImportError
from .db.db import get_session


class Importer:

    def __init__(self):
        self.session = get_session()
        self.baby_repo = BabyRepository(self.session)
        self.caregiver_repo = CaregiverRepository(self.session)
        self.diaper_change_repo = DiaperChangeRepository(self.session)
        self.milk_feed_repo = MilkFeedRepository(self.session)
        self.pump_repo = PumpRepository(self.session)

    def import_models(self, models: ModelResults):
        with self.session as session:
            session.add_all(models.babies)
            session.add_all(models.caregivers)
            session.add_all(models.bottles)
            session.add_all(models.diapers)
            session.add_all(models.pumps)
            session.commit()

    # TODO make this async after getting it working
    def validate_inserts(self, models: ModelResults) -> list[ModelImportError]:
        errors = []

        if self.baby_repo.count() != len(models.babies):
            errors.append(
                ModelImportError("Baby", len(models.babies), self.baby_repo.count())
            )

        if self.caregiver_repo.count() != len(models.caregivers):
            errors.append(
                ModelImportError(
                    "Caregiver", len(models.caregivers), self.caregiver_repo.count()
                )
            )

        if self.milk_feed_repo.count() != len(models.bottles):
            errors.append(
                ModelImportError(
                    "MilkFeed", len(models.bottles), self.milk_feed_repo.count()
                )
            )

        if self.diaper_change_repo.count() != len(models.diapers):
            errors.append(
                ModelImportError(
                    "DiaperChange", len(models.diapers), self.diaper_change_repo.count()
                )
            )

        if self.pump_repo.count() != len(models.pumps):
            errors.append(
                ModelImportError("Pump", len(models.pumps), self.pump_repo.count())
            )

        return errors
