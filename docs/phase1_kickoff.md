# Phase 1 Kickoff & Handoff

*swlegion-meta · Written at end of Phase 0 planning, before Phase 1 build sessions · v0.1*

**If you are Claude Code, or any future Claude session, or a collaborator:** read this doc first. It captures the current state of the project, the key Phase 0 decisions that shape Phase 1 building work, and immediate next actions. Reference the docs listed at the bottom for full detail on any topic.

---

## Current status

**Phase 0 (Foundation & Discovery): COMPLETE.** All eight groups (A–J) done. Public GitHub repo scaffolded, CI green, vision drafted, data source dossier complete, canonical schema designed and refactored to SQLModel, legal/data-usage doc drafted, Longshanks outreach sent (no response received after 6+ weeks — treating as silent no), newsletter plan drafted.

**Phase 1 (Ingest + Baseline): IN PROGRESS, Session 1.**

- **Step 1: `uv add sqlmodel`** — ✅ done
- **Step 2: Refactor `schemas/canonical_v0.py` to SQLModel** — ✅ done, CI green
- **Step 3: Create `db.py` (engine + session setup)** — ✅ done (`src/swlegion_meta/db.py`)
- **Step 4: Create `ingest.py` (CSV ingest CLI)** — ✅ done (`src/swlegion_meta/ingest.py`, tests in `tests/test_ingest.py`)
- **Step 5: Design CSV template for personal games entry** — ✅ done (`data/raw/personal_games_template.csv`). **Next: Session 2 — fill in the CSV.**

---

## Phase 1 goals (revised under Plan B)

Original scope from `docs/roadmap.md` Phase 1 was "one data source in, canonical DB populated, first public artifact." Under Plan B (no Longshanks partnership), this translates to:

1. **Load Justin's ~350 games of legitimately-yours-or-consented data** into local SQLite via CSV ingest
2. **Get analytical infrastructure working end-to-end** — DB, queries, EDA notebook
3. **Ship Newsletter Issue 1** with real numbers from Justin's data (see `docs/sample_newsletter_issue_1.md` for the format template)
4. **Design and build the community submission flow** so teammates and future community users can add games via a simple form

Phase 1 exit criteria in the roadmap: "One-command ingest works. First public content out." Both still apply.

---

## Key Phase 0 decisions that shape Phase 1 building

Don't re-litigate these; they're settled and captured in docs. Building work should be consistent with them.

### Product positioning (from `docs/vision.md`)
- **Prescriptive, predictive, and personal-longitudinal** analytics layer on top of the descriptive picture Longshanks provides. NOT trying to be a better meta stats site — Longshanks/Fifth Trooper own that.
- **Primary persona:** mid-tier competitive players trying to break into top of RTT/regional scene
- **Secondary persona:** meta/GT chasers (credibility layer)
- **Flagship feature:** personal longitudinal analytics tied to specific list changes ("your win rate improved from 45% to 58% since you swapped Grievous for Dooku")

### Scope discipline (from `docs/vision.md` non-goals)
- **We consume list URLs from Tabletop Admiral / Legion List Builder; we NEVER build lists ourselves.** If a user wants to change a list, they go to TA/LLB, edit there, re-share the URL. This friction is a feature — enforces our scope permanently.
- No beginner tutorial content
- No community forum / social platform
- No rules/errata reference

### Data foundation (from `docs/data_sources.md`)
- **Primary source: community submissions** (user-uploaded via our tool)
- **Founder seed data:** Justin's ~125 personal Longshanks tournament games (Sep 2023 onward) + ~200-280 games from consented teammates + potentially 31 RBDG games (with caveats, see below)
- **Meta Read for newsletter:** Fifth Trooper aggregate stats (cited), podcasts, Reddit synthesis
- **Longshanks: silent no.** Do not scrape, do not aggregate their event data even manually. Their published data-export policy (`docs/data_usage.md` and the article Justin shared) makes clear that aggregating win rates / results is against their policy even when manual. The only carve-outs are (a) copying player-submitted army lists as game-piece data, and (b) copying pairings during an event for utility use.

### Schema (from `docs/schema.md` and `schemas/canonical_v0.py`)
- **Game is the atom.** Everything else is metadata on the Game.
- **ListIdentity + ListSnapshot pattern** (Moxfield/Archidekt style) — identity persists, snapshots version.
- **Ruleset versioning is critical.** Every Game, Event, and ListSnapshot tags the ruleset it was played under. Never mix pre/post-patch data without explicit filter.
- **Users and Players are separate entities.** Opponents in submitted games are often Players without a User account.
- **Source tracking:** every record carries a `source` field (community_submitted, longshanks_partnership, tta_oauth, llb_oauth, official, founder_historical) — the FOUNDER_HISTORICAL enum was added specifically for Justin's imported personal games.

### Tech stack decisions
- Python 3.10 (upgrade to 3.11+ optional later)
- `uv` for dependency management
- **SQLModel** for ORM (chosen for Pydantic reuse + easy Postgres migration path in Phase 4)
- SQLite for Phase 1-3; migrate to Supabase Postgres in Phase 4
- Streamlit for the interactive app (Phase 3)
- **Beehiiv** for the newsletter (Phase 2 launch)
- GitHub Actions for CI

---

## Immediate next actions (Phase 1 Session 1, Steps 3-5)

### Step 3: Create `src/swlegion_meta/db.py` (or `scripts/db.py`)

Session/engine management for SQLite. Should include:

- SQLite engine setup pointing at `data/swlegion_meta.db` (this file is gitignored via `data/*` in `.gitignore`)
- `create_db_and_tables()` function that uses `SQLModel.metadata.create_all(engine)` to bootstrap the schema
- `get_session()` context manager for query operations
- Small helper `init_db()` that creates the DB file and all tables if they don't exist

Package structure decision: Justin's repo has `src/swlegion_meta/` from `uv init`. Files should live there for proper packaging. If `scripts/` was used earlier for anything, that's fine — but new modules go in `src/swlegion_meta/`.

### Step 4: Create `src/swlegion_meta/ingest.py`

CSV ingest CLI. Should support:

```
uv run python -m swlegion_meta.ingest --file data/raw/personal_games.csv
```

Ingest logic:
1. Read CSV rows
2. For each row, upsert Event (by name+date), upsert Player (by longshanks_id or display_name), upsert ListIdentity (by player_id + display_name), create new ListSnapshot per row (with version_hash based on composition or list_name+ruleset for MVP), create Game
3. For opponents whose list we don't know (common in casual games), create a minimal ListSnapshot with just faction, source_platform=MANUAL, empty composition_json — this satisfies FK constraints without forcing data we don't have
4. Bad rows fail loudly with clear error messages
5. Idempotent — re-running the same CSV shouldn't duplicate rows (use deterministic IDs from a hash of stable fields, or check-then-insert)

### Step 5: Design and create `data/raw/personal_games_template.csv`

CSV columns for manual entry (target: minimize typing, ~15-16 columns):

- `date` (played_at date)
- `event_name` (blank for casual)
- `ruleset_version` (e.g., "2.6", required)
- `round` (blank for casual)
- `game_type` (casual/tournament_rated/tournament_unrated/practice/league/playtest)
- `my_list_name` (e.g., "Han Gunline v3")
- `my_faction`
- `opponent_name` (blank for unknown)
- `opponent_faction`
- `objective`
- `deployment`
- `condition`
- `my_score`
- `opponent_score`
- `outcome` (win/loss/tie/incomplete — can be derived from scores if provided)
- `notes` (optional)

Include one example row filled in so Justin has a reference.

### Add tests
- `tests/test_db.py` — verifies DB init works, tables get created
- `tests/test_ingest.py` — verifies CSV ingest with a small fixture file, checks that Games/Players/ListIdentities land correctly

---

## Path through Phase 1 after Session 1

**Session 2 (~2-3 hours, Justin's manual work, not Claude Code work):**
- Sit down with own Longshanks profile (browsing his own account = unambiguously fine)
- Fill in the CSV row by row for his 125 personal games
- Batch by tournament to copy event-level fields once per event
- Run ingest, verify data lands correctly

**Session 3 (~90 min):**
- First EDA notebook in `notebooks/` — explore the loaded data
- Faction win rates, scenario patterns, deployment-level analysis, list evolution
- This is where the "surprising finding" for Newsletter Issue 1 will emerge

**Session 4-5 (~2-3 hours):**
- Draft Newsletter Issue 1 based on real EDA findings (structure per `docs/sample_newsletter_issue_1.md`)
- Set up Beehiiv account, configure sender identity
- Publish Issue 1 (soft launch — Reddit, Discord, competitive Facebook groups)

**Session 6+:**
- Community submission flow (form-based MVP, no auth yet — can use Google Forms as a v0 that pipes to CSV, then upgrade to native form once auth exists)
- Teammate outreach with consent message (draft this soon)
- Second EDA cut, Newsletter Issue 2

Phase 1 exit criteria (from `docs/roadmap.md`):
- One-command ingest works end-to-end ✓ when Session 1 done
- Notebook polished enough for a stranger to skim and get the point ✓ when Session 3 done
- At least one post is live linking back to the repo ✓ when Issue 1 shipped

---

## What NOT to do (constraints from Phase 0 work)

- **Do not scrape Longshanks.** Not automated, not manual, not "just a little." Justin already made the ethical commitment via outreach ("if the answer is 'please don't scrape,' I'll design around it"). Their published policy is explicit that aggregating results and win rates is against their intent even when done by hand. Only Justin's own games and consented teammate data are on the table.
- **Do not integrate RBDG data casually.** The 31 RBDG battle report games may or may not be usable — Justin needs to have an explicit conversation with RBDG partners before including them. Default position: don't include unless explicit "yes this is fine" received. This project stays personal, RBDG stays RBDG.
- **Do not build a list construction UI.** Ever. Users paste TA/LLB URLs; that's the interface. If a feature request smells like "let me tweak this list here," redirect them back to TA/LLB. Scope discipline is what keeps this product from becoming a worse version of tools that already exist.
- **Do not blend pre/post-patch data in analysis.** Every query filters by `ruleset_version`. Mixing eras produces misleading trends and burns credibility.
- **Do not promote paid tier in Newsletter Issues 1-3.** Paid tier doesn't exist yet. Soft footer mentions start Issue 4-6. See `docs/newsletter_plan.md` for the full phased strategy.

---

## Where to find context

Sorted by likelihood you'll need it:

- **`docs/roadmap.md`** — master roadmap for Phase 1-5, checklist state for Phase 0, deployment topology, delivery cycle per feature
- **`docs/vision.md`** — product brief, personas, tiers, non-goals, success metrics, open decisions
- **`docs/schema.md`** — schema design rationale, entity overview diagram, design principles, rejected alternatives
- **`schemas/canonical_v0.py`** — the actual SQLModel definitions (source of truth for the data model)
- **`docs/data_sources.md`** — dossier of every data source, scoring, legal status, contingencies
- **`docs/data_usage.md`** — per-source legal reads, community submission consent intent, escalation triggers
- **`docs/newsletter_plan.md`** — full newsletter plan (positioning, structure, cadence, platform, voice, promotion strategy, distribution, success metrics, production workflow)
- **`docs/sample_newsletter_issue_1.md`** — sample Issue 1 with voice + structure realized, template for real Issue 1
- **`docs/longshanks_email_draft.md`** — v3 draft that was sent, kept for reference
- **`docs/backlog.md`** — Phase 1+ backlog with prioritization principle
- **`tests/test_schema.py`** — sanity test showing the schema in use

---

## Phase 1 exit criteria (paste from `docs/roadmap.md`)

- One-command ingest works end-to-end
- Notebook polished enough for a stranger to skim and get the point
- At least one public post (Newsletter Issue 1) is live linking back to the repo
- Data validation tests exist (bad rows fail loudly)

When all four are met, Phase 1 is done. Tag repo `v0.2.0-phase1-complete`, ship the launch post that was deferred from Group J, move to Phase 2.

---

*Version history*
- v0.1 · End of Phase 0 planning — initial kickoff doc for Phase 1 build work, includes handoff context for Claude Code or any future session
