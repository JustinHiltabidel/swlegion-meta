"""Sanity tests for the canonical schema.

Proves the schema can represent a real tournament game end-to-end.
If these tests fail, the schema is broken — fix it before doing anything else.
"""

from datetime import date, datetime, timezone

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
    SubscriptionTier,
    Unit,
    UnitRank,
    Upgrade,
    User,
)

RULESET = "2.6"  # placeholder — replace with current when known


# ============================================================================
# Sanity: construct one real-ish tournament game end-to-end
# ============================================================================


def test_sanity_full_tournament_game():
    """Round 3 of a hypothetical GT: Rebels vs Empire.

    If the schema can round-trip this without errors, it can represent
    the real-world use cases we designed for.
    """
    # --- The two players ---
    alex = Player(
        id="player_alex",
        display_name="AlexP",
        faction_prefs=[Faction.REBELS, Faction.REPUBLIC],
        region="Midwest US",
        longshanks_id=None,
        created_at=datetime(2026, 1, 15, 10, 0, tzinfo=timezone.utc),
    )
    beck = Player(
        id="player_beck",
        display_name="BeckJ",
        faction_prefs=[Faction.EMPIRE],
        region="Midwest US",
        longshanks_id=None,
        created_at=datetime(2026, 2, 1, 14, 30, tzinfo=timezone.utc),
    )

    # --- Alex is a paid user; Beck is not a user of our platform ---
    alex_user = User(
        id="user_alex",
        email="alex@example.com",
        tier=SubscriptionTier.PAID,
        linked_player_id=alex.id,
        created_at=datetime(2026, 3, 1, 9, 0, tzinfo=timezone.utc),
    )

    # --- The event ---
    event = Event(
        id="event_adepticon_2026_gt",
        name="Adepticon 2026 Legion GT",
        date=date(2026, 3, 22),
        location="Schaumburg, IL",
        format="1000pt Standard",
        ruleset_version=RULESET,
        size=64,
        source=DataSource.COMMUNITY_SUBMITTED,
        longshanks_event_id=None,  # partnership TBD
    )

    # --- Alex's list: identity + snapshot ---
    alex_list_identity = ListIdentity(
        id="list_id_alex_han_gunline",
        player_id=alex.id,
        display_name="Han Gunline v3",
        faction=Faction.REBELS,
        created_at=datetime(2026, 2, 10, 20, 0, tzinfo=timezone.utc),
        retired_at=None,
    )
    alex_list_snapshot = ListSnapshot(
        id="snap_alex_han_v3_march",
        identity_id=alex_list_identity.id,
        composition_json={
            "faction": "rebels",
            "points": 1000,
            "commander": {"name": "Han Solo", "points": 120},
            "corps": [
                {"name": "Rebel Troopers", "count": 4, "upgrades": ["Z-6"]},
            ],
            # ...abbreviated for the test
        },
        points=1000,
        version_hash="sha256:abc123...",
        source_url="https://tabletopadmiral.com/legion/list/xyz789",
        source_platform=SourcePlatform.TABLETOP_ADMIRAL,
        ruleset_version=RULESET,
        created_at=datetime(2026, 3, 20, 22, 15, tzinfo=timezone.utc),  # tweaked night before
        is_current=True,
    )

    # --- Beck's list: identity + snapshot ---
    beck_list_identity = ListIdentity(
        id="list_id_beck_krennic",
        player_id=beck.id,
        display_name="Krennic Death Star",
        faction=Faction.EMPIRE,
        created_at=datetime(2026, 2, 5, 19, 0, tzinfo=timezone.utc),
        retired_at=None,
    )
    beck_list_snapshot = ListSnapshot(
        id="snap_beck_krennic_march",
        identity_id=beck_list_identity.id,
        composition_json={
            "faction": "empire",
            "points": 1000,
            "commander": {"name": "Director Krennic", "points": 90},
            # ...abbreviated
        },
        points=1000,
        version_hash="sha256:def456...",
        source_url="https://tabletopadmiral.com/legion/list/abc123",
        source_platform=SourcePlatform.TABLETOP_ADMIRAL,
        ruleset_version=RULESET,
        created_at=datetime(2026, 3, 15, 21, 0, tzinfo=timezone.utc),
        is_current=True,
    )

    # --- The game itself ---
    game = Game(
        id="game_adepticon_2026_r3_table_5",
        event_id=event.id,
        round=3,
        player_a_id=alex.id,
        player_b_id=beck.id,
        list_a_snapshot_id=alex_list_snapshot.id,
        list_b_snapshot_id=beck_list_snapshot.id,
        objective="Bombing Run",
        deployment="Advanced Positions",
        condition="War of Attrition",
        outcome=GameOutcome.PLAYER_A_WIN,
        score_a=8,
        score_b=6,
        game_type=GameType.TOURNAMENT_RATED,
        played_at=datetime(2026, 3, 22, 13, 45, tzinfo=timezone.utc),
        ruleset_version=RULESET,
        source=DataSource.COMMUNITY_SUBMITTED,
        notes="Alex clutched Round 6 with Han's ambush; Krennic stayed pinned.",
        submitted_by_user_id=alex_user.id,
        created_at=datetime(2026, 3, 22, 22, 10, tzinfo=timezone.utc),
    )

    # --- All entities constructed and validated. Confirm key relationships. ---
    assert game.event_id == event.id
    assert game.player_a_id == alex.id
    assert game.player_b_id == beck.id
    assert game.list_a_snapshot_id == alex_list_snapshot.id
    assert game.list_b_snapshot_id == beck_list_snapshot.id
    assert alex_list_snapshot.identity_id == alex_list_identity.id
    assert beck_list_snapshot.identity_id == beck_list_identity.id
    assert alex_user.linked_player_id == alex.id
    assert game.outcome == GameOutcome.PLAYER_A_WIN


# ============================================================================
# Additional edge cases the schema must handle
# ============================================================================


def test_casual_game_has_no_event():
    """Casual games at the shop have no event or round — must be nullable."""
    alex = Player(
        id="player_alex", display_name="AlexP", created_at=datetime(2026, 1, 1, tzinfo=timezone.utc)
    )
    beck = Player(
        id="player_beck", display_name="BeckJ", created_at=datetime(2026, 1, 1, tzinfo=timezone.utc)
    )
    alex_list = ListSnapshot(
        id="snap_alex_casual",
        identity_id="list_alex_1",
        composition_json={},
        points=800,
        version_hash="h1",
        source_platform=SourcePlatform.MANUAL,
        ruleset_version=RULESET,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    beck_list = ListSnapshot(
        id="snap_beck_casual",
        identity_id="list_beck_1",
        composition_json={},
        points=800,
        version_hash="h2",
        source_platform=SourcePlatform.MANUAL,
        ruleset_version=RULESET,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    game = Game(
        id="game_casual_1",
        event_id=None,  # ← nullable
        round=None,  # ← nullable
        player_a_id=alex.id,
        player_b_id=beck.id,
        list_a_snapshot_id=alex_list.id,
        list_b_snapshot_id=beck_list.id,
        objective="Key Positions",
        deployment="Battle Lines",
        condition="Rapid Reinforcements",
        outcome=GameOutcome.PLAYER_B_WIN,
        score_a=4,
        score_b=7,
        game_type=GameType.CASUAL,
        played_at=datetime(2026, 4, 5, 19, 30, tzinfo=timezone.utc),
        ruleset_version=RULESET,
        source=DataSource.COMMUNITY_SUBMITTED,
        created_at=datetime(2026, 4, 5, 22, 0, tzinfo=timezone.utc),
    )

    assert game.event_id is None
    assert game.round is None
    assert game.game_type == GameType.CASUAL


def test_opponent_without_user_account():
    """Opponents in submitted games often exist as Players without a User."""
    opponent = Player(
        id="player_random_bob",
        display_name="Bob from the shop",
        created_at=datetime(2026, 5, 1, tzinfo=timezone.utc),
    )
    # No User is required. The Player exists on its own.
    assert opponent.display_name == "Bob from the shop"


def test_reference_catalog_versioned():
    """Units and upgrades are versioned by ruleset — same unit across
    rulesets is two records, not one, so trend analysis doesn't blur eras."""
    han_2_6 = Unit(
        id="unit_han_solo_2_6",
        name="Han Solo",
        faction=Faction.REBELS,
        rank=UnitRank.COMMANDER,
        base_points=120,
        ruleset_version="2.6",
    )
    han_3_0 = Unit(
        id="unit_han_solo_3_0",
        name="Han Solo",
        faction=Faction.REBELS,
        rank=UnitRank.COMMANDER,
        base_points=110,  # hypothetical repricing
        ruleset_version="3.0",
    )
    assert han_2_6.base_points != han_3_0.base_points
    assert han_2_6.name == han_3_0.name

    z6 = Upgrade(
        id="upg_z6_2_6",
        name="Z-6 Trooper",
        category="heavy_weapon",
        points=32,
        ruleset_version="2.6",
    )
    assert z6.points == 32
