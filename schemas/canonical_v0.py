"""Canonical schema v0 for swlegion-meta.

Every Game is the atom; everything else is metadata. Design decisions and
rationale live in docs/schema.md — read that first if the "why" matters.

Uses SQLModel to serve two purposes at once: Pydantic validation (as DTOs)
and SQLAlchemy ORM (as persisted tables). Every entity here is marked
table=True and becomes a real database table.

Version: 0.3
Changelog:
  - 0.2 (Phase 1 Session 1): Converted from pure Pydantic to SQLModel to
        support persistence. All entities now table=True with primary keys,
        foreign keys, and JSON columns for complex fields. Added
        FOUNDER_HISTORICAL to DataSource for imported founder game data.
  - 0.3 (Phase 1 Session 1): Game scenario fields match the current mission
        structure — objective/deployment/condition replaced by primary_mission,
        secondary_mission, advantage_a, advantage_b. Added Game.conceded.
  - 0.1 (Day 2 of Phase 0): Initial draft. Six entities + two reference
        tables. ListIdentity + ListSnapshot pattern (Moxfield/Archidekt style).
"""

from datetime import date, datetime, timezone
from enum import Enum

from pydantic import EmailStr
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

UTC = timezone.utc


# ============================================================================
# Enums — constrained value sets
# ============================================================================


class Faction(str, Enum):
    """Star Wars: Legion factions."""

    REBELS = "rebels"
    EMPIRE = "empire"
    REPUBLIC = "republic"
    SEPARATISTS = "separatists"
    SHADOW_COLLECTIVE = "shadow_collective"
    MERCENARIES = "mercenaries"


class UnitRank(str, Enum):
    """Unit rank slots in a Legion army list."""

    COMMANDER = "commander"
    OPERATIVE = "operative"
    CORPS = "corps"
    SPECIAL_FORCES = "special_forces"
    SUPPORT = "support"
    HEAVY = "heavy"


class SubscriptionTier(str, Enum):
    """User subscription tiers."""

    FREE = "free"
    PAID = "paid"
    PREMIUM = "premium"


class SourcePlatform(str, Enum):
    """Where a list was constructed."""

    TABLETOP_ADMIRAL = "tabletop_admiral"
    LEGION_LIST_BUILDER = "legion_list_builder"
    MANUAL = "manual"


class DataSource(str, Enum):
    """Provenance of a Game, Event, or ListSnapshot record."""

    COMMUNITY_SUBMITTED = "community_submitted"
    LONGSHANKS_PARTNERSHIP = "longshanks_partnership"
    TTA_OAUTH = "tta_oauth"
    LLB_OAUTH = "llb_oauth"
    OFFICIAL = "official"
    FOUNDER_HISTORICAL = "founder_historical"  # imported by Justin from own tournament history


class GameType(str, Enum):
    """Nature of the game — determines analytical weight."""

    TOURNAMENT_RATED = "tournament_rated"
    TOURNAMENT_UNRATED = "tournament_unrated"
    CASUAL = "casual"
    PRACTICE = "practice"
    LEAGUE = "league"
    PLAYTEST = "playtest"


class GameOutcome(str, Enum):
    """Result of a game."""

    PLAYER_A_WIN = "player_a_win"
    PLAYER_B_WIN = "player_b_win"
    TIE = "tie"
    INCOMPLETE = "incomplete"


# ============================================================================
# Core entities
# ============================================================================


class User(SQLModel, table=True):
    """An account holder in swlegion-meta."""

    id: str = Field(primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    tier: SubscriptionTier = Field(default=SubscriptionTier.FREE)
    linked_player_id: str | None = Field(default=None, foreign_key="player.id")
    created_at: datetime


class Player(SQLModel, table=True):
    """Someone who plays games. May or may not be a User.

    Opponents in submitted games often exist as Players without User accounts —
    they're just names + faction until/unless they sign up.
    """

    id: str = Field(primary_key=True)
    display_name: str
    faction_prefs: list[Faction] = Field(default_factory=list, sa_column=Column(JSON))
    region: str | None = None
    longshanks_id: str | None = Field(default=None, unique=True, index=True)
    created_at: datetime


class Event(SQLModel, table=True):
    """Optional container for games. Casual play has no event."""

    id: str = Field(primary_key=True)
    name: str
    date: date
    location: str | None = None
    format: str  # e.g., "1000pt Standard", "GT 800pt"
    ruleset_version: str
    size: int | None = None
    source: DataSource
    longshanks_event_id: str | None = Field(default=None, index=True)


# ============================================================================
# List identity + snapshot pattern (Moxfield/Archidekt-style)
# ============================================================================


class ListIdentity(SQLModel, table=True):
    """The persistent identity of a list — 'my Krennic Death Star' as a
    continuous thing across all its versions."""

    id: str = Field(primary_key=True)
    player_id: str = Field(foreign_key="player.id", index=True)
    display_name: str
    faction: Faction
    created_at: datetime
    retired_at: datetime | None = None


class ListSnapshot(SQLModel, table=True):
    """A specific composition at a moment in time.

    New snapshot created when composition changes. Games reference specific
    snapshots so the exact table state is preserved for analysis.
    """

    id: str = Field(primary_key=True)
    identity_id: str = Field(foreign_key="listidentity.id", index=True)
    composition_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
    points: int
    version_hash: str = Field(index=True)  # fingerprint for dedup / same-list detection
    source_url: str | None = None
    source_platform: SourcePlatform
    ruleset_version: str
    created_at: datetime
    is_current: bool = True


# ============================================================================
# Game — the atom
# ============================================================================


class Game(SQLModel, table=True):
    """A match. Everything else in the schema is metadata on this."""

    id: str = Field(primary_key=True)

    # Container (nullable — casual games have neither)
    event_id: str | None = Field(default=None, foreign_key="event.id", index=True)
    round: int | None = None

    # Who played, with what
    player_a_id: str = Field(foreign_key="player.id", index=True)
    player_b_id: str = Field(foreign_key="player.id", index=True)
    list_a_snapshot_id: str = Field(foreign_key="listsnapshot.id")
    list_b_snapshot_id: str = Field(foreign_key="listsnapshot.id")

    # Mission setup — free-form strings for now; likely enum once real data flows.
    # Advantage cards are chosen per player; B's is often unknown.
    primary_mission: str = Field(index=True)
    secondary_mission: str = Field(index=True)
    advantage_a: str = Field(index=True)
    advantage_b: str | None = Field(default=None, index=True)

    # Outcome
    outcome: GameOutcome
    score_a: int | None = None
    score_b: int | None = None
    conceded: bool = False  # loser (per outcome) conceded before the game finished

    # Context
    game_type: GameType = Field(index=True)
    played_at: datetime = Field(index=True)  # WHEN — critical for trend analysis
    ruleset_version: str = Field(index=True)
    source: DataSource

    # Freeform
    notes: str | None = None

    # Provenance
    submitted_by_user_id: str | None = Field(default=None, foreign_key="user.id")
    created_at: datetime


# ============================================================================
# Reference tables — canonical Legion catalog
# ============================================================================


class Unit(SQLModel, table=True):
    """Canonical Legion unit — for lookups and analysis.

    Populated from AMG official data. Versioned by ruleset so trend analysis
    doesn't blur pre/post-balance-patch data.
    """

    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    faction: Faction = Field(index=True)
    rank: UnitRank
    base_points: int
    ruleset_version: str = Field(index=True)


class Upgrade(SQLModel, table=True):
    """Canonical Legion upgrade card. Versioned by ruleset."""

    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    category: str
    points: int
    ruleset_version: str = Field(index=True)
