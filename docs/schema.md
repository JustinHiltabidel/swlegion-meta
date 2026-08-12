# Canonical Schema v0

*swlegion-meta · Group I deliverable · Phase 0 · v0.1*

## Purpose

Define the core data model for the product. Every downstream analysis — trend analysis, matchup stats, list scoring, simulator training — queries against this schema. Get it right at Phase 0; changing it later is expensive.

## Design principle: the Game is the atom

Every meaningful analytical question in this product resolves to "look at Games with property X and compute Y." Personal meta, matchup breakdowns, trend analysis, simulator training — all queries on Games. Every other entity in the schema is metadata that describes a Game or groups Games together.

Design accordingly: the Game record must be self-sufficient enough to be interesting on its own, and richly-linked enough to power any grouping we want later.

## Entity overview

```
User ────── (linked to) ──────► Player
                                   │
                                   │ owns
                                   ▼
Event ─── (optional) ─── Game ─── ListIdentity ─── (many) ── ListSnapshot
   ▲                       │                                       │
   │                       │ uses                                  │ composition
   │                       ▼                                       ▼
   │              ListSnapshot × 2                           JSON (units, upgrades)
   │              (list_a, list_b)                                  │
   │                                                                │
   └──── (all timestamped by ruleset_version) ─────────────────────┘

              Unit + Upgrade catalogs — lookup tables, versioned by ruleset
```

## Entities

### User
Account holder in the product. `id`, `email`, `tier` (free/paid/premium), `linked_player_id` (nullable — who they are in-game), `created_at`.

### Player
Someone who plays games. May or may not be a User. Opponents in submitted games often exist as Players without accounts. `id`, `display_name`, `faction_prefs`, `region`, `longshanks_id` (nullable for future partnership), `created_at`.

### Event
Optional container for games. Casual/practice games have no Event. `id`, `name`, `date`, `location`, `format`, `ruleset_version`, `size`, `source`, `longshanks_event_id` (nullable).

### ListIdentity
The **persistent identity** of a list — "my Krennic Death Star" as a continuous thing the user names and browses, even as the composition drifts. `id`, `player_id`, `display_name`, `faction`, `created_at`, `retired_at` (nullable, soft-delete).

### ListSnapshot
A **specific composition at a moment in time**. New snapshot when composition changes. Games reference specific snapshots so the exact table state is preserved. `id`, `identity_id`, `composition_json` (parsed TA/LLB JSON), `points`, `version_hash` (dedup fingerprint), `source_url`, `source_platform`, `ruleset_version`, `created_at`, `is_current`.

### Game
The atom. `id`, `event_id` (nullable), `round` (nullable), `player_a_id`, `player_b_id`, `list_a_snapshot_id`, `list_b_snapshot_id`, `objective`, `deployment`, `condition`, `outcome`, `score_a`, `score_b`, `game_type`, `played_at`, `ruleset_version`, `source`, `notes`, `submitted_by_user_id`, `created_at`.

### Unit + Upgrade (reference tables)
Canonical catalog data from AMG. Versioned by ruleset so trend analysis doesn't blur pre/post-balance data.

## Design decisions and rationale

**1. ListIdentity + ListSnapshot pattern (borrowed from Moxfield/Archidekt).**

Two entities, not one. Identity is what the user names. Snapshots are versions. Games reference snapshots so exact state is preserved; the library UI groups snapshots by identity.

This pattern:
- Matches the user's mental model ("my Krennic list" persists across tweaks)
- Enables both cross-version trend analysis ("my Krennic list overall") and within-version trend analysis ("my current build since I swapped Grievous for Dooku")
- Keeps storage modest — new snapshot only when composition actually changes
- Makes list import natural: hash the incoming JSON, match to an existing snapshot on any of the user's identities, otherwise prompt "update existing list or new list?"

**2. Timestamps on everything.**

`played_at` on Game, `created_at` on every entity. Trend analysis is the flagship feature; "when" must be first-class. `played_at` and `created_at` are deliberately separate on Game — a user can log a game they played last week.

**3. Nullable relationships where honest.**

- Event nullable on Game — casual play has no event
- Round nullable on Game — same reason
- User's `linked_player_id` nullable — a user might browse content without identifying themselves in-game
- Player's `longshanks_id` nullable — most Players won't have one
- Player has no required User link — opponents exist as Players without accounts

Nullables are chosen deliberately, not sprinkled. Every nullable field represents a real "sometimes this doesn't exist" case in the domain.

**4. Source tracking on data.**

Every Game, Event, and ListSnapshot carries a `source` field (`community_submitted`, `longshanks_partnership`, `tta_oauth`, `llb_oauth`, `official`). Downstream analysis filters by provenance — a user might want "only my logged games" or "only tournament data" and this makes those queries trivial.

**5. Ruleset versioning.**

Every Game, Event, and ListSnapshot tags the ruleset version it was played under. Legion 2.6 vs 3.0 changes unit points, cards, sometimes rules. Without versioning, trend analysis crosses eras and produces misleading results. `Unit` and `Upgrade` reference tables also carry ruleset_version so a lookup during analysis returns the correct-era stats.

**6. JSON blob for list composition.**

`ListSnapshot.composition_json` stores the full parsed TA/LLB JSON. We don't normalize it into `list_units` / `list_upgrades` tables — the JSON is the truth, extract fields to columns lazily as queries demand. Reanalyze without refetching.

**7. Users and Players are separate.**

Some Players in the database will never be Users; opponents in submitted games are just names + faction. If they later sign up, we merge Player into User via `linked_player_id`. This keeps the "log a game against Bob at the shop" workflow trivial without forcing every Bob to have an account.

## Rejected alternatives

**Single flat List entity (no identity/snapshot split).** Rejected — either produces duplicate records for every tweak (storage waste, breaks the user's mental model of "my list") or overwrites in place (destroys trend analysis).

**Reference-only Lists with mutable composition.** Rejected — Games would lose the exact composition on the table by the time analysis runs. Trend analysis becomes impossible if edits overwrite.

**Snapshot per Game (my original suggestion).** Rejected in favor of Identity+Snapshot after founder feedback. Snapshot-per-Game bloats storage (new snapshot every game, even with no changes) and loses the user's persistent-identity mental model.

## Sanity test

The schema must be able to represent one real tournament game end-to-end. See `tests/test_schema.py` for a fully populated example: Rebels vs Empire, Round 3 of a GT, all fields filled.

## Open items for v0.2 and beyond

- **Unit/Upgrade catalog population** — needs AMG data source (Phase 1 work)
- **Objective / Deployment / Condition enumeration** — currently free-form strings; likely wants an enum or reference table once we have real data (Phase 1 refinement)
- **Multi-round tournaments** — Events don't yet model round structure; may need a `Round` entity if we want to query "how did you do in Round 3s across all your events"
- **Team events** — schema assumes 1v1; team formats would need extension
- **Non-standard scenarios** — narrative games, special formats not currently modeled

## Version history

- **v0.1** · Day 2 of Phase 0 — initial draft. Six entities + two reference tables. ListIdentity + ListSnapshot pattern. Ready for Phase 1 refinement based on real data.
