"""DB bootstrap tests — the schema must create cleanly on a fresh SQLite file."""

from sqlalchemy import inspect

from swlegion_meta.db import get_session, init_db, make_engine

EXPECTED_TABLES = {
    "user",
    "player",
    "event",
    "listidentity",
    "listsnapshot",
    "game",
    "unit",
    "upgrade",
}


def test_init_db_creates_all_tables(tmp_path):
    db_path = tmp_path / "nested" / "test.db"
    engine = init_db(db_path)

    assert db_path.exists()
    assert EXPECTED_TABLES <= set(inspect(engine).get_table_names())


def test_init_db_is_rerunnable(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    engine = init_db(db_path)  # second call must not fail or wipe anything
    assert EXPECTED_TABLES <= set(inspect(engine).get_table_names())


def test_foreign_keys_enforced():
    engine = make_engine(":memory:")
    with get_session(engine) as session:
        assert session.connection().exec_driver_sql("PRAGMA foreign_keys").scalar() == 1
