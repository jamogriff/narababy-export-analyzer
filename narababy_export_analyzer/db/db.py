import os
from pathlib import Path
from platformdirs import user_data_dir
from sqlalchemy import create_engine, select, func, text, Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from ..models.baby import Baby

APP_NAME = "nb-data-analysis"
AUTHOR = "jamogriff"
DB_FILENAME = "export.db"

# Internal singleton engine
_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None

def get_database_path() -> Path:
    return Path(user_data_dir(APP_NAME, AUTHOR)) / DB_FILENAME

def initialize_database() -> bool:
    global _engine

    db_path = get_database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove database if it exists
    if db_path.exists():
        os.remove(db_path)

        for ext in (".db-wal", ".db-shm"):
            extra = db_path.with_suffix(ext)
            if extra.exists():
                os.remove(extra)

    try:
        _engine = get_engine()
        # Create dummy table and delete it to trigger
        # creation of database file
        with _engine.begin() as conn:
            conn.execute(text("CREATE TABLE __init__ (id INTEGER)"))
            conn.execute(text("DROP TABLE __init__"))

        return True
    except OperationalError:
        _engine = None
        return False

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        db_path = get_database_path()
        _engine = create_engine(f"sqlite+pysqlite:///{db_path}", echo=False)
    return _engine

def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _SessionLocal()

def does_data_exist() -> bool:
    with get_session() as session:
        stmt = select(func.count()).select_from(Baby)
        try:
            count = session.execute(stmt).scalar_one()
        except OperationalError:
            count = 0

    return count > 0

