"""CSV ingest tests — correct loading, idempotency, and loud failure on bad rows."""

from pathlib import Path

import pytest
from sqlmodel import select

from schemas.canonical_v0 import (
    DataSource,
    Event,
    Faction,
    Game,
    GameOutcome,
    ListIdentity,
    ListSnapshot,
    Player,
)
from swlegion_meta.db import get_session, init_db
from swlegion_meta.ingest import IngestError, ingest_file, main, read_csv

FIXTURE = Path(__file__).parent / "fixtures" / "games_small.csv"
TEMPLATE = Path(__file__).parent.parent / "data" / "raw" / "personal_games_template.csv"
HEADER = FIXTURE.read_text().splitlines()[0]


@pytest.fixture
def engine(tmp_path):
    return init_db(tmp_path / "test.db")


def write_csv(tmp_path, *rows: str) -> Path:
    path = tmp_path / "games.csv"
    path.write_text("\n".join([HEADER, *rows]) + "\n")
    return path


def test_ingest_loads_games_players_and_lists(engine):
    result = ingest_file(FIXTURE, engine, "Justin")

    assert result.games_added == 3
    assert result.events_added == 1  # both tournament rounds share one event
    with get_session(engine) as s:
        games = s.exec(select(Game).order_by(Game.played_at, Game.round)).all()
        assert [g.outcome for g in games] == [
            GameOutcome.PLAYER_A_WIN,  # derived from 8-6 with blank outcome
            GameOutcome.PLAYER_B_WIN,
            GameOutcome.TIE,
        ]
        assert all(g.player_a_id == "player_justin" for g in games)
        assert all(g.source == DataSource.FOUNDER_HISTORICAL for g in games)
        assert games[2].event_id is None and games[2].round is None

        names = {p.display_name for p in s.exec(select(Player)).all()}
        assert names == {"Justin", "Beck", "Casey", "Unknown opponent"}

        event = s.exec(select(Event)).one()
        assert event.name == "Spring RTT"

        my_lists = s.exec(
            select(ListIdentity).where(ListIdentity.player_id == "player_justin")
        ).all()
        assert len(my_lists) == 1
        assert my_lists[0].faction == Faction.REBELS

        # Changing the list URL between games produced a second snapshot; the newer one is current.
        snaps = s.exec(
            select(ListSnapshot).where(ListSnapshot.identity_id == my_lists[0].id)
        ).all()
        assert len(snaps) == 2
        current = [snap for snap in snaps if snap.is_current]
        assert len(current) == 1
        assert current[0].source_url.endswith("/b")


def test_aliases_normalize_factions(engine):
    ingest_file(FIXTURE, engine, "Justin")
    with get_session(engine) as s:
        casey = s.get(Player, "player_casey")
        lists = s.exec(
            select(ListIdentity).where(ListIdentity.player_id == casey.id)
        ).all()
        assert lists[0].faction == Faction.SEPARATISTS


def test_ingest_is_idempotent(engine):
    ingest_file(FIXTURE, engine, "Justin")
    second = ingest_file(FIXTURE, engine, "Justin")

    assert second.games_added == 0
    assert second.games_skipped == 3
    with get_session(engine) as s:
        assert len(s.exec(select(Game)).all()) == 3
        assert len(s.exec(select(Player)).all()) == 4
        assert len(s.exec(select(ListSnapshot)).all()) == 5


def test_bad_rows_fail_loudly_and_load_nothing(engine, tmp_path):
    path = write_csv(
        tmp_path,
        "2026-03-22,Spring RTT,2.6,1,tournament_rated,Han,rebels,,Beck,empire,Bombing Run,Battle Lines,Clear,8,6,,",
        "03/22/2026,Spring RTT,2.6,2,tournament_rated,Han,rebels,,Beck,wookiees,Bombing Run,Battle Lines,Clear,8,6,,",
        "2026-03-22,,2.6,3,tournament_rated,Han,rebels,,Beck,empire,Bombing Run,Battle Lines,Clear,8,6,loss,",
    )
    with pytest.raises(IngestError) as exc:
        ingest_file(path, engine, "Justin")

    message = str(exc.value)
    assert "2 bad row(s)" in message
    assert "line 3" in message and "YYYY-MM-DD" in message and "wookiees" in message
    assert "line 4" in message and "event_name" in message and "contradicts" in message
    with get_session(engine) as s:
        assert s.exec(select(Game)).all() == []


def test_missing_columns_rejected(tmp_path):
    path = tmp_path / "games.csv"
    path.write_text("date,my_faction\n2026-01-01,rebels\n")
    with pytest.raises(IngestError, match="missing columns"):
        read_csv(path)


def test_template_parses():
    rows = read_csv(TEMPLATE)
    assert len(rows) == 1
    assert rows[0].outcome == GameOutcome.PLAYER_A_WIN


def test_cli_end_to_end(tmp_path, capsys):
    db = tmp_path / "cli.db"
    assert main(["--file", str(FIXTURE), "--player", "Justin", "--db", str(db)]) == 0
    assert "games added:     3" in capsys.readouterr().out
    assert db.exists()
