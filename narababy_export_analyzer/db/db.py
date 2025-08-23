from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

def does_database_exist(engine) -> bool:
    try:
        with engine.connect() as conn:
            return True
    except OperationalError:
        return False

