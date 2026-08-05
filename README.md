# swlegion-meta

Data-driven tools and analysis for the competitive Star Wars: Legion community.

## What this is

A tiered data product for tournament-level Legion players. Free newsletter for meta commentary, subscription tier for list-building tools, premium tier for predictive matchup models. Built on tournament data from Longshanks, community submissions, and public event coverage.

## Status

🚧 **Phase 0 — Foundation & Discovery.** Data source dossier, canonical schema, and repo scaffolding in progress. No app or ingest pipeline yet.

## Product tiers (planned)

- **Free** — Biweekly newsletter with meta trends, tournament recaps, and unit-level analysis.
- **Paid** — Interactive list scorer, matchup planner, personalized dashboard for uploaded games.
- **Premium** — Predictive game outcome models, opponent list simulation, deep matchup explorer.

## Tech stack

- Python 3.10+ with `uv` for dependency management
- Jupyter for exploratory analysis
- SQLite (v1) → Postgres via Supabase (v2)
- Streamlit for the interactive app
- GitHub Actions for scheduled data ingest and CI

## Repository structure

```
data/         Local data storage (gitignored)
notebooks/    Jupyter notebooks — EDA, modeling, analysis
scripts/      Ingest, scraping, and utility scripts
app/          Streamlit application
schemas/      Canonical data models
docs/         Vision, data sources, architecture notes
tests/        Unit + integration tests
```

## Roadmap

Full roadmap and phase-by-phase execution plan lives in `docs/roadmap.md` (coming Phase 0).

## License

MIT — see `LICENSE`.
