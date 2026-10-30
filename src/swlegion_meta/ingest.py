"""CSV ingest for personal / founder game history.

Usage:
    uv run python -m swlegion_meta.ingest --file data/raw/personal_games.csv --player "Justin"

Each CSV row is one game from the point of view of `--player` (always player A).
See data/raw/personal_games_template.csv for the column layout.

Guarantees:
  - All rows are validated before anything is written. Any bad row aborts the
    whole file with a per-row error report — nothing half-loads.
  - Idempotent. IDs are derived from stable row fields, so re-running the same
    CSV (or a CSV with new rows appended) never duplicates records.
"""

import argparse
import csv
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from pathlib import Path

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from schemas.canonical_v0 import (
    DataSource,
    Event,
    Faction,
    Game,
    GameOutcome,
    GameType,
    ListIdentity,
    ListSnapshot,
    Player,
    SourcePlatform,
)
from swlegion_meta.db import DEFAULT_DB_PATH, get_session, init_db

UTC = timezone.utc

REQUIRED_COLUMNS = [
    "date",
    "event_name",
    "ruleset_version",
    "round",
    "game_type",
    "list_name",
    "faction",
    "opponent_faction",
    "primary_mission",
    "secondary_mission",
    "advantage",
    "opponent_advantage",
    "score",
    "opponent_score",
    "outcome",
    "notes",
]
OPTIONAL_COLUMNS = ["list_url", "conceded"]

FACTION_ALIASES = {
    "rebel": Faction.REBELS,
    "imperial": Faction.EMPIRE,
    "imperials": Faction.EMPIRE,
    "gar": Faction.REPUBLIC,
    "cis": Faction.SEPARATISTS,
    "separatist": Faction.SEPARATISTS,
    "seps": Faction.SEPARATISTS,
    "sc": Faction.SHADOW_COLLECTIVE,
    "mercs": Faction.MERCENARIES,
    "mercenary": Faction.MERCENARIES,
}

OUTCOME_ALIASES = {
    "win": GameOutcome.PLAYER_A_WIN,
    "w": GameOutcome.PLAYER_A_WIN,
    "loss": GameOutcome.PLAYER_B_WIN,
    "l": GameOutcome.PLAYER_B_WIN,
    "tie": GameOutcome.TIE,
    "draw": GameOutcome.TIE,
    "t": GameOutcome.TIE,
    "incomplete": GameOutcome.INCOMPLETE,
}

TRUE_VALUES = {"x", "yes", "y", "true", "t", "1"}
FALSE_VALUES = {"", "no", "n", "false", "f", "0"}

# Opponents are never named — every game is against this single placeholder
# player, so the stored data carries no third-party identities.
ANONYMOUS_OPPONENT = "Anonymous opponent"


class IngestError(Exception):
    """Raised when one or more CSV rows fail validation."""


@dataclass
class ParsedRow:
    line: int
    played_on: date
    event_name: str | None
    ruleset_version: str
    round: int | None
    game_type: GameType
    list_name: str
    faction: Faction
    list_url: str | None
    opponent_faction: Faction
    primary_mission: str
    secondary_mission: str
    advantage: str
    opponent_advantage: str | None
    score: int | None
    opponent_score: int | None
    outcome: GameOutcome
    conceded: bool
    notes: str | None
    fingerprint: str  # hash of the whole normalized row — the game's identity


@dataclass
class IngestResult:
    games_added: int = 0
    games_skipped: int = 0
    players_added: int = 0
    events_added: int = 0
    lists_added: int = 0
    snapshots_added: int = 0


# ============================================================================
# Helpers
# ============================================================================


def _hash(*parts: object) -> str:
    joined = "\x1f".join("" if p is None else str(p) for p in parts)
    return hashlib.sha256(joined.encode()).hexdigest()[:16]


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def _norm_key(text: str) -> str:
    return re.sub(r"[\s\-]+", "_", text.strip().lower())


def parse_faction(raw: str) -> Faction:
    key = _norm_key(raw)
    try:
        return Faction(key)
    except ValueError:
        pass
    if key in FACTION_ALIASES:
        return FACTION_ALIASES[key]
    valid = ", ".join(f.value for f in Faction)
    raise ValueError(f"unknown faction {raw!r} (expected one of: {valid})")


def parse_game_type(raw: str) -> GameType:
    try:
        return GameType(_norm_key(raw))
    except ValueError:
        valid = ", ".join(g.value for g in GameType)
        raise ValueError(
            f"unknown game_type {raw!r} (expected one of: {valid})"
        ) from None


def _parse_int(raw: str, column: str) -> int | None:
    raw = raw.strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"{column} must be a whole number, got {raw!r}") from None


def parse_bool(raw: str, column: str) -> bool:
    key = raw.strip().lower()
    if key in TRUE_VALUES:
        return True
    if key in FALSE_VALUES:
        return False
    raise ValueError(f"{column} must be X/yes/true or blank, got {raw!r}")


def resolve_outcome(
    raw: str, my_score: int | None, opp_score: int | None, conceded: bool = False
) -> GameOutcome:
    """Use the outcome column if given, else derive from scores. Both given → must agree.

    A conceded game must be a win or loss, and its outcome must be given explicitly:
    the score at concession time doesn't decide the result.
    """
    if conceded:
        outcome = OUTCOME_ALIASES.get(raw.strip().lower())
        if outcome not in (GameOutcome.PLAYER_A_WIN, GameOutcome.PLAYER_B_WIN):
            raise ValueError("conceded games need outcome win or loss")
        return outcome

    from_scores = None
    if my_score is not None and opp_score is not None:
        if my_score > opp_score:
            from_scores = GameOutcome.PLAYER_A_WIN
        elif my_score < opp_score:
            from_scores = GameOutcome.PLAYER_B_WIN
        else:
            from_scores = GameOutcome.TIE

    raw = raw.strip().lower()
    if not raw:
        if from_scores is None:
            raise ValueError(
                "outcome is blank and scores are incomplete — provide one or the other"
            )
        return from_scores

    if raw not in OUTCOME_ALIASES:
        raise ValueError(f"unknown outcome {raw!r} (expected win/loss/tie/incomplete)")
    explicit = OUTCOME_ALIASES[raw]
    # Score ties can still be decided on tiebreakers, so only flag a hard contradiction.
    contradicts = (
        from_scores is not None
        and from_scores != GameOutcome.TIE
        and explicit != from_scores
    )
    if explicit != GameOutcome.INCOMPLETE and contradicts:
        raise ValueError(f"outcome {raw!r} contradicts score {my_score}-{opp_score}")
    return explicit


def parse_row(row: dict[str, str], line: int) -> ParsedRow:
    """Validate one CSV row. Raises ValueError listing every problem found."""
    row = {k: (v or "").strip() for k, v in row.items() if k is not None}
    problems: list[str] = []

    def required(column: str) -> str:
        value = row.get(column, "")
        if not value:
            problems.append(f"{column} is required")
        return value

    def attempt(fn, *args):
        try:
            return fn(*args)
        except ValueError as e:
            problems.append(str(e))
            return None

    played_on = None
    raw_date = required("date")
    if raw_date:
        try:
            played_on = date.fromisoformat(raw_date)
        except ValueError:
            problems.append(f"date must be YYYY-MM-DD, got {raw_date!r}")

    ruleset_version = required("ruleset_version")
    raw_game_type = required("game_type")
    game_type = attempt(parse_game_type, raw_game_type) if raw_game_type else None
    list_name = required("list_name")
    raw_faction = required("faction")
    faction = attempt(parse_faction, raw_faction) if raw_faction else None
    raw_opp_faction = required("opponent_faction")
    opp_faction = attempt(parse_faction, raw_opp_faction) if raw_opp_faction else None
    primary_mission = required("primary_mission")
    secondary_mission = required("secondary_mission")
    advantage = required("advantage")

    round_ = attempt(_parse_int, row.get("round", ""), "round")
    score = attempt(_parse_int, row.get("score", ""), "score")
    opp_score = attempt(_parse_int, row.get("opponent_score", ""), "opponent_score")
    conceded = attempt(parse_bool, row.get("conceded", ""), "conceded")
    outcome = attempt(
        resolve_outcome, row.get("outcome", ""), score, opp_score, bool(conceded)
    )

    event_name = row.get("event_name") or None
    if (
        game_type in (GameType.TOURNAMENT_RATED, GameType.TOURNAMENT_UNRATED)
        and not event_name
    ):
        problems.append("tournament games need an event_name")

    if problems:
        raise ValueError("; ".join(problems))

    normalized = [row.get(c, "") for c in REQUIRED_COLUMNS + OPTIONAL_COLUMNS]
    return ParsedRow(
        line=line,
        played_on=played_on,
        event_name=event_name,
        ruleset_version=ruleset_version,
        round=round_,
        game_type=game_type,
        list_name=list_name,
        faction=faction,
        list_url=row.get("list_url") or None,
        opponent_faction=opp_faction,
        primary_mission=primary_mission,
        secondary_mission=secondary_mission,
        advantage=advantage,
        opponent_advantage=row.get("opponent_advantage") or None,
        score=score,
        opponent_score=opp_score,
        outcome=outcome,
        conceded=conceded,
        notes=row.get("notes") or None,
        fingerprint=_hash(*normalized),
    )


def read_csv(path: Path) -> list[ParsedRow]:
    """Parse and validate every row. Raises IngestError with all failures at once."""
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise IngestError(f"{path}: missing columns: {', '.join(missing)}")

        parsed: list[ParsedRow] = []
        errors: list[str] = []
        for line, row in enumerate(reader, start=2):  # line 1 is the header
            if not any((v or "").strip() for v in row.values() if isinstance(v, str)):
                continue  # blank line
            try:
                parsed.append(parse_row(row, line))
            except ValueError as e:
                errors.append(f"  line {line}: {e}")

    if errors:
        raise IngestError(
            f"{path}: {len(errors)} bad row(s), nothing was loaded:\n"
            + "\n".join(errors)
        )
    return parsed


# ============================================================================
# Upserts — insert if missing, otherwise leave the existing record alone
# ============================================================================


def _played_at(d: date) -> datetime:
    return datetime.combine(d, time(0, 0), tzinfo=UTC)


def _get_or_add(
    session: Session, model, record_id: str, factory, result: IngestResult, counter: str
):
    existing = session.get(model, record_id)
    if existing is not None:
        return existing
    record = factory()
    session.add(record)
    session.flush()
    setattr(result, counter, getattr(result, counter) + 1)
    return record


def _player(
    session: Session, name: str, created: datetime, result: IngestResult
) -> Player:
    pid = f"player_{_slug(name)}"
    return _get_or_add(
        session,
        Player,
        pid,
        lambda: Player(id=pid, display_name=name, created_at=created),
        result,
        "players_added",
    )


def _event(
    session: Session, r: ParsedRow, source: DataSource, result: IngestResult
) -> Event:
    eid = f"event_{_slug(r.event_name)}_{r.played_on.isoformat()}"
    return _get_or_add(
        session,
        Event,
        eid,
        lambda: Event(
            id=eid,
            name=r.event_name,
            date=r.played_on,
            format="Standard",
            ruleset_version=r.ruleset_version,
            source=source,
        ),
        result,
        "events_added",
    )


def _identity(
    session: Session,
    player: Player,
    name: str,
    faction: Faction,
    created: datetime,
    result: IngestResult,
) -> ListIdentity:
    lid = f"list_{_hash(player.id, name)}"
    return _get_or_add(
        session,
        ListIdentity,
        lid,
        lambda: ListIdentity(
            id=lid,
            player_id=player.id,
            display_name=name,
            faction=faction,
            created_at=created,
        ),
        result,
        "lists_added",
    )


def _snapshot(
    session: Session,
    identity: ListIdentity,
    r: ParsedRow,
    url: str | None,
    points: int,
    result: IngestResult,
) -> ListSnapshot:
    # MVP fingerprint: no parsed composition yet, so list name + ruleset + URL stand in.
    version_hash = _hash(identity.display_name, r.ruleset_version, url)
    sid = f"snap_{_hash(identity.id, version_hash)}"
    snap = _get_or_add(
        session,
        ListSnapshot,
        sid,
        lambda: ListSnapshot(
            id=sid,
            identity_id=identity.id,
            composition_json={"faction": identity.faction.value},
            points=points,
            version_hash=version_hash,
            source_url=url,
            source_platform=_platform_for(url),
            ruleset_version=r.ruleset_version,
            created_at=_played_at(r.played_on),
        ),
        result,
        "snapshots_added",
    )
    # Snapshot "created" = first game it was seen in, regardless of CSV order.
    if snap.created_at.replace(tzinfo=UTC) > _played_at(r.played_on):
        snap.created_at = _played_at(r.played_on)
    return snap


def _platform_for(url: str | None) -> SourcePlatform:
    if url and "tabletopadmiral" in url:
        return SourcePlatform.TABLETOP_ADMIRAL
    if url and "legion" in url and "builder" in url:
        return SourcePlatform.LEGION_LIST_BUILDER
    return SourcePlatform.MANUAL


def _refresh_current_snapshots(session: Session, identity_ids: set[str]) -> None:
    """Exactly one snapshot per identity is current: the most recently first-seen one."""
    for identity_id in identity_ids:
        snaps = session.exec(
            select(ListSnapshot).where(ListSnapshot.identity_id == identity_id)
        ).all()
        latest = max(snaps, key=lambda s: (s.created_at.replace(tzinfo=UTC), s.id))
        for s in snaps:
            s.is_current = s.id == latest.id


def ingest_rows(
    session: Session,
    rows: list[ParsedRow],
    player_name: str,
    source: DataSource = DataSource.FOUNDER_HISTORICAL,
    default_points: int = 1000,
) -> IngestResult:
    result = IngestResult()
    now = datetime.now(UTC)
    touched_identities: set[str] = set()

    me = _player(session, player_name, now, result)
    opponent = _player(session, ANONYMOUS_OPPONENT, now, result)

    for r in rows:
        game_id = f"game_{r.fingerprint}"
        if session.get(Game, game_id) is not None:
            result.games_skipped += 1
            continue

        event = _event(session, r, source, result) if r.event_name else None
        played_at = _played_at(r.played_on)

        my_identity = _identity(session, me, r.list_name, r.faction, played_at, result)
        # Opponent lists are unknown and anonymous — one placeholder identity per
        # faction satisfies the FKs without inventing composition.
        opp_list_name = f"{r.opponent_faction.value} (list unknown)"
        opp_identity = _identity(
            session, opponent, opp_list_name, r.opponent_faction, played_at, result
        )

        my_snap = _snapshot(session, my_identity, r, r.list_url, default_points, result)
        opp_snap = _snapshot(session, opp_identity, r, None, default_points, result)
        touched_identities.update({my_identity.id, opp_identity.id})

        session.add(
            Game(
                id=game_id,
                event_id=event.id if event else None,
                round=r.round,
                player_a_id=me.id,
                player_b_id=opponent.id,
                list_a_snapshot_id=my_snap.id,
                list_b_snapshot_id=opp_snap.id,
                primary_mission=r.primary_mission,
                secondary_mission=r.secondary_mission,
                advantage_a=r.advantage,
                advantage_b=r.opponent_advantage,
                outcome=r.outcome,
                conceded=r.conceded,
                score_a=r.score,
                score_b=r.opponent_score,
                game_type=r.game_type,
                played_at=played_at,
                ruleset_version=r.ruleset_version,
                source=source,
                notes=r.notes,
                created_at=now,
            )
        )
        session.flush()
        result.games_added += 1

    _refresh_current_snapshots(session, touched_identities)
    return result


def ingest_file(
    path: Path,
    engine: Engine,
    player_name: str,
    source: DataSource = DataSource.FOUNDER_HISTORICAL,
    default_points: int = 1000,
) -> IngestResult:
    rows = read_csv(path)
    with get_session(engine) as session:
        return ingest_rows(session, rows, player_name, source, default_points)


# ============================================================================
# CLI
# ============================================================================


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Ingest a personal games CSV into the local DB."
    )
    parser.add_argument("--file", required=True, type=Path, help="CSV file to ingest")
    parser.add_argument(
        "--player", required=True, help="Your display name (player A in every row)"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"SQLite path (default {DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--source",
        default=DataSource.FOUNDER_HISTORICAL.value,
        choices=[s.value for s in DataSource],
        help="Provenance tag for every record",
    )
    parser.add_argument(
        "--points", type=int, default=1000, help="List points when not otherwise known"
    )
    args = parser.parse_args(argv)

    if not args.file.exists():
        print(f"error: {args.file} does not exist", file=sys.stderr)
        return 1

    engine = init_db(args.db)
    try:
        result = ingest_file(
            args.file, engine, args.player, DataSource(args.source), args.points
        )
    except IngestError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(
        f"Ingested {args.file} → {args.db}\n"
        f"  games added:     {result.games_added}\n"
        f"  games skipped:   {result.games_skipped} (already loaded)\n"
        f"  players added:   {result.players_added}\n"
        f"  events added:    {result.events_added}\n"
        f"  lists added:     {result.lists_added}\n"
        f"  snapshots added: {result.snapshots_added}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
