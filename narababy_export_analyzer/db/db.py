from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..models.baby import Baby

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)

def does_database_exist(engine) -> bool:
    try:
        with engine.connect() as conn:
            return True
    except OperationalError:
        return False

def does_data_exist(engine) -> bool:
    if not does_database_exist(engine):
        return False

    with Session(engine) as session:
        stmt = select(func.count()).select_from(Baby)
        try:
            count = session.execute(stmt).scalar_one()
        except OperationalError:
            count = 0

    return count > 0

