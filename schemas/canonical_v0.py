"""Canonical schema v0 for swlegion-meta.

Every Game is the atom; everything else is metadata. Design decisions and
rationale live in docs/schema.md — read that first if the "why" matters.

Version: 0.1
Changelog:
  - 0.1 (Day 2 of Phase 0): Initial draft. Six entities + two reference
        tables. ListIdentity + ListSnapshot pattern (Moxfield/Archidekt style).
        Timestamps everywhere, source tracking, ruleset versioning.
"""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field

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


class User(BaseModel):
    """An account holder in swlegion-meta."""

    id: str
    email: EmailStr
    tier: SubscriptionTier = SubscriptionTier.FREE
    linked_player_id: str | None = None  # who they are in-game
    created_at: datetime


class Player(BaseModel):
    """Someone who plays games. May or may not be a User.

    Opponents in submitted games often exist as Players without User accounts —
    they're just names + faction until/unless they sign up.
    """

    id: str
    display_name: str
    faction_prefs: list[Faction] = Field(default_factory=list)
    region: str | None = None
    longshanks_id: str | None = None  # nullable — future partnership integration
    created_at: datetime


class Event(BaseModel):
    """Optional container for games. Casual play has no event."""

    id: str
    name: str
    date: date
    location: str | None = None
    format: str  # e.g., "1000pt Standard", "GT 800pt"
    ruleset_version: str  # e.g., "2.6", "3.0"
    size: int | None = None  # player count
    source: DataSource
    longshanks_event_id: str | None = None  # nullable — partnership integration


# ============================================================================
# List identity + snapshot pattern (Moxfield/Archidekt-style)
# ============================================================================


class ListIdentity(BaseModel):
    """The persistent identity of a list — 'my Krennic Death Star' as a
    continuous thing across all its versions.

    This is what the user names, browses in their library, and thinks of as
    one thing even as the composition drifts. Games reference ListSnapshots
    (below), which are linked back to an identity.
    """

    id: str
    player_id: str
    display_name: str  # user-chosen: "Krennic Death Star", "my main Sep list"
    faction: Faction
    created_at: datetime
    retired_at: datetime | None = None  # user marks retired (soft-delete)


class ListSnapshot(BaseModel):
    """A specific composition at a moment in time.

    New snapshot created when composition changes. Games reference specific
    snapshots so the exact table state is preserved for analysis.
    """

    id: str
    identity_id: str
    composition_json: dict  # parsed TA/LLB JSON — full unit + upgrade structure
    points: int
    version_hash: str  # fingerprint for dedup / same-list detection
    source_url: str | None = None  # TA or LLB URL if imported
    source_platform: SourcePlatform
    ruleset_version: str
    created_at: datetime
    is_current: bool = True  # only one snapshot per identity is "current"


# ============================================================================
# Game — the atom
# ============================================================================


class Game(BaseModel):
    """A match. Everything else in the schema is metadata on this."""

    id: str

    # Container (nullable — casual games have neither)
    event_id: str | None = None
    round: int | None = None

    # Who played, with what
    player_a_id: str
    player_b_id: str
    list_a_snapshot_id: str
    list_b_snapshot_id: str

    # Scenario — currently free-form strings; likely enum in v0.2
    objective: str
    deployment: str
    condition: str

    # Outcome
    outcome: GameOutcome
    score_a: int | None = None
    score_b: int | None = None

    # Context
    game_type: GameType
    played_at: datetime  # WHEN — critical for trend analysis
    ruleset_version: str
    source: DataSource

    # Freeform
    notes: str | None = None

    # Provenance
    submitted_by_user_id: str | None = None
    created_at: datetime


# ============================================================================
# Reference tables — canonical Legion catalog
# ============================================================================


class Unit(BaseModel):
    """Canonical Legion unit — for lookups and analysis.

    Populated from AMG official data. Versioned by ruleset so trend analysis
    doesn't blur pre/post-balance-patch data.
    """

    id: str
    name: str
    faction: Faction
    rank: UnitRank
    base_points: int
    ruleset_version: str


class Upgrade(BaseModel):
    """Canonical Legion upgrade card. Versioned by ruleset."""

    id: str
    name: str
    category: str  # weapon, gear, grenade, personnel, force, comms, etc.
    points: int
    ruleset_version: str
