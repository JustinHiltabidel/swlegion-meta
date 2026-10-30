"""SQLite engine and session management.

Phase 1-3 run on a local SQLite file. Phase 4 swaps the URL for Supabase
Postgres — nothing else here should need to change.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

# Importing the schema registers every table on SQLModel.metadata.
import schemas.canonical_v0  # noqa: F401

DEFAULT_DB_PATH = Path("data/swlegion_meta.db")


def make_engine(db_path: Path | str = DEFAULT_DB_PATH, echo: bool = False) -> Engine:
    """Build an engine for a SQLite file. Pass ":memory:" for tests."""
    if str(db_path) == ":memory:":
        url = "sqlite://"
    else:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        url = f"sqlite:///{db_path}"
    engine = create_engine(url, echo=echo)

    # SQLite ignores foreign keys unless asked per connection.
    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, _record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def create_db_and_tables(engine: Engine) -> None:
    """Create every table in the canonical schema that doesn't exist yet."""
    SQLModel.metadata.create_all(engine)


def init_db(db_path: Path | str = DEFAULT_DB_PATH) -> Engine:
    """Create the DB file (if needed) and all tables. Returns the engine."""
    engine = make_engine(db_path)
    create_db_and_tables(engine)
    return engine


@contextmanager
def get_session(engine: Engine) -> Iterator[Session]:
    """Session that commits on success and rolls back on any error."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
