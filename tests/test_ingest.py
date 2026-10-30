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

    assert result.games_added == 4
    assert result.events_added == 1  # all tournament rounds share one event
    with get_session(engine) as s:
        games = s.exec(select(Game).order_by(Game.played_at, Game.round)).all()
        assert [g.outcome for g in games] == [
            GameOutcome.PLAYER_A_WIN,  # derived from 8-6 with blank outcome
            GameOutcome.PLAYER_B_WIN,
            GameOutcome.PLAYER_A_WIN,  # opponent conceded while ahead on points
            GameOutcome.TIE,
        ]
        assert [g.conceded for g in games] == [False, False, True, False]
        assert games[0].primary_mission == "Primary A"
        assert games[0].advantage_a == "Advantage A"
        assert games[0].advantage_b == "Advantage B"
        assert games[1].advantage_b is None
        assert all(g.player_a_id == "player_justin" for g in games)
        assert all(g.source == DataSource.FOUNDER_HISTORICAL for g in games)
        assert games[3].event_id is None and games[3].round is None

        # Opponents are anonymized: one placeholder player, no names stored.
        names = {p.display_name for p in s.exec(select(Player)).all()}
        assert names == {"Justin", "Anonymous opponent"}
        assert {g.player_b_id for g in games} == {"player_anonymous_opponent"}

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
        lists = s.exec(
            select(ListIdentity).where(
                ListIdentity.player_id == "player_anonymous_opponent"
            )
        ).all()
        assert {li.faction for li in lists} == {
            Faction.EMPIRE,
            Faction.SEPARATISTS,
            Faction.SHADOW_COLLECTIVE,
        }


def test_ingest_is_idempotent(engine):
    ingest_file(FIXTURE, engine, "Justin")
    second = ingest_file(FIXTURE, engine, "Justin")

    assert second.games_added == 0
    assert second.games_skipped == 4
    with get_session(engine) as s:
        assert len(s.exec(select(Game)).all()) == 4
        assert len(s.exec(select(Player)).all()) == 2
        assert len(s.exec(select(ListSnapshot)).all()) == 5


def test_bad_rows_fail_loudly_and_load_nothing(engine, tmp_path):
    path = write_csv(
        tmp_path,
        "2026-03-22,Spring RTT,2.6,1,tournament_rated,Han,rebels,,empire,P,S,A,,8,6,,,",
        "03/22/2026,Spring RTT,2.6,2,tournament_rated,Han,rebels,,wookiees,P,S,A,,8,6,,,",
        "2026-03-22,,2.6,3,tournament_rated,Han,rebels,,empire,P,S,A,,8,6,loss,,",
        "2026-03-22,Spring RTT,2.6,4,tournament_rated,Han,rebels,,empire,P,S,,,8,6,tie,maybe,",
    )
    with pytest.raises(IngestError) as exc:
        ingest_file(path, engine, "Justin")

    message = str(exc.value)
    assert "3 bad row(s)" in message
    assert "line 3" in message and "YYYY-MM-DD" in message and "wookiees" in message
    assert "line 4" in message and "event_name" in message and "contradicts" in message
    assert "line 5" in message and "advantage is required" in message
    assert "conceded must be X/yes/true" in message
    with get_session(engine) as s:
        assert s.exec(select(Game)).all() == []


def test_conceded_tie_rejected(tmp_path):
    path = write_csv(
        tmp_path,
        "2026-04-05,,2.6,,casual,Han,rebels,,empire,P,S,A,,5,5,tie,yes,",
    )
    with pytest.raises(IngestError, match="conceded games need outcome win or loss"):
        read_csv(path)


def test_missing_columns_rejected(tmp_path):
    path = tmp_path / "games.csv"
    path.write_text("date,faction\n2026-01-01,rebels\n")
    with pytest.raises(IngestError, match="missing columns"):
        read_csv(path)


def test_template_parses():
    rows = read_csv(TEMPLATE)
    assert len(rows) == 1
    assert rows[0].outcome == GameOutcome.PLAYER_A_WIN


def test_cli_end_to_end(tmp_path, capsys):
    db = tmp_path / "cli.db"
    assert main(["--file", str(FIXTURE), "--player", "Justin", "--db", str(db)]) == 0
    assert "games added:     4" in capsys.readouterr().out
    assert db.exists()
