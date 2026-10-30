# swlegion-meta
![CI](https://github.com/JustinHiltabidel/swlegion-meta/actions/workflows/ci.yml/badge.svg)

Data-driven tools and analysis for the competitive Star Wars: Legion community.

## What this is

A tiered data product for tournament-level Legion players. Free newsletter for meta commentary, paid tier for prescriptive decision-support tools (list scoring, matchup planning, personal longitudinal analytics), premium tier for predictive matchup simulation. Built on user-submitted game data with the founder's own tournament history as seed data.

## Status

🚀 **Phase 1 — Ingest + Baseline.** Phase 0 (Foundation & Discovery) complete: vision, data source dossier, canonical schema, legal/data-usage doc, newsletter plan, and Longshanks outreach all shipped. Now building the ingest pipeline for founder + community game data, aiming for first newsletter issue and public artifact from real numbers.

## Product tiers (planned)

- **Free** — Biweekly newsletter with meta commentary and personal analyst notebook content
- **Paid** — Interactive list scorer, matchup planner, archetype playbooks
- **Premium** — Predictive matchup simulator, personal longitudinal analytics tied to specific list changes

## Tech stack

- Python 3.10+ with `uv` for dependency management
- SQLModel (Pydantic + SQLAlchemy) for schema and persistence
- SQLite for Phase 1–3 → Supabase Postgres in Phase 4
- Jupyter for exploratory analysis
- Streamlit for the interactive app (Phase 3+)
- Beehiiv for the newsletter (Phase 2 launch)
- GitHub Actions for CI

## Repository structure

```
data/         Local data storage (gitignored)
notebooks/    Jupyter notebooks — EDA, modeling, analysis
scripts/      Utility scripts
src/          Application code (swlegion_meta package)
app/          Streamlit application (Phase 3+)
schemas/      Canonical data models (SQLModel)
docs/         Vision, roadmap, data sources, schema, newsletter plan, backlog
tests/        Unit + integration tests
```

## Roadmap

Full roadmap and phase-by-phase execution plan lives in `docs/roadmap.md`. For anyone (or any Claude session) picking up the work, start with `docs/phase1_kickoff.md`.

## License

MIT — see `LICENSE`.
