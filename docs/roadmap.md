# Star Wars Legion Data Product
## Development Roadmap — v1.0

---

### Vision
A tiered data product for the competitive Star Wars: Legion community. Free newsletter builds the audience, subscription tier delivers prescriptive list-building tools, premium tier delivers predictive matchup models. Distinct from The Fifth Trooper by going beyond descriptive meta reporting into decision-support tooling.

### Product tiers
- **Free** — Newsletter (weekly or biweekly). Deep meta commentary, faction/unit trends, tournament recaps with real numbers.
- **Paid ($5–10/mo)** — Prescriptive tools. List scorer, matchup planner, personalized dashboard for community-submitted games.
- **Premium ($15–25/mo)** — Predictive layer. Game outcome models, opponent list simulation, deep matchup explorer.

### Data strategy (three legs, no single point of failure)
1. **Longshanks** — pursue partnership/read access first. Fallback: limited scraping within stated bounds.
2. **Community submissions** — moat + legal path. Users upload their own games in exchange for analysis.
3. **Public supplements** — BCP, event recaps, YouTube batrep transcripts, GT threads.

### Tech stack (v1 — favor speed over sophistication)
- Language: Python
- Storage: SQLite → Postgres when it hurts
- Notebooks: Jupyter (analysis), pushed to GitHub
- App: Streamlit → deployed via Streamlit Cloud or Hugging Face Spaces
- Newsletter: Substack or Beehiiv (don't build a CMS)
- Auth/payments (Phase 3+): Patreon or Stripe + magic-link auth
- Version control: GitHub, public repo
- CI: GitHub Actions (lint + tests) — set up in Phase 0, don't skip

---

## Phase 0 — Foundation & Discovery
**Weeks 1–3 · Goal: Know what you're building and what data you can legally get.**

Deliverables
- Public GitHub repo scaffolded (`/data`, `/notebooks`, `/scripts`, `/app`, `/docs`)
- `docs/vision.md` — one-page product brief
- `docs/data_sources.md` — every source scored on volume, legality, effort, reliability
- `schemas/canonical_v0.py` — first draft of the standard game record
- Longshanks outreach email sent
- CI pipeline running (lint, basic tests)

Exit criteria
- You can explain the product to a stranger in 2 minutes
- You have a written data plan with backup routes
- Repo is public and someone googling you finds a real project skeleton

Key risks
- Longshanks says no with a hard boundary → community-submission timeline pulls forward
- Schema too rigid early → keep v0 minimal, iterate

---

## Phase 1 — Ingest + Baseline
**Weeks 4–8 · Goal: One data source in, canonical DB populated, first public artifact.**

Deliverables
- CSV ingest CLI (`python -m legion.ingest --source csv --file path/to/data.csv`)
- SQLite DB seeded with 5–10 tournaments (manual entry OK if scraping isn't ready)
- EDA notebook — faction win rates, list archetype clusters, top units
- First public post (LinkedIn + repo README) with real numbers and one insight
- Data validation tests — bad rows fail loudly

Exit criteria
- One-command ingest works end-to-end
- Notebook is polished enough for a stranger to skim and get the point
- At least one post is live linking back to the repo

Key risks
- Manual seed data biases early analysis → note it explicitly, don't over-claim
- Schema needs a break early → do it now while data volume is tiny

---

## Phase 2 — Automated Ingest + Content Loop
**Weeks 9–14 · Goal: Data grows without manual work. Newsletter live with real subscribers.**

Deliverables
- First automated ingest — scraper for whichever source has clearest legal terms (likely BCP or event recap threads)
- Scheduled pulls (weekly cron or manual trigger + logging)
- Newsletter live on Substack/Beehiiv with 3–4 issues out
- Community wait-list (email capture on newsletter landing page)
- Second data source integrated behind canonical schema
- `docs/architecture.md` — how sources plug in

Exit criteria
- Dataset grows week over week without you doing anything
- Newsletter has real subscribers (target: 100)
- Analytical layer is genuinely source-agnostic

Key risks
- Scraper breaks silently → build failure alerts (email or Discord webhook)
- Newsletter feels thin → lean on real analysis, not opinion — that's your edge

---

## Phase 3 — Prescriptive App MVP + First Revenue
**Weeks 15–22 · Goal: Interactive tool live. Paid tier launched. First paying user.**

Deliverables
- List scoring model v1 (rule-based + descriptive stats, not ML yet)
- Streamlit app with list input → analysis output, deployed publicly
- Community submission form (Google Form → DB is fine for v1)
- Paid tier launched on Patreon or Stripe
- Landing page tying free → paid together
- 3 more newsletter issues, at least one referencing the app

Exit criteria
- App URL you can share
- Someone paid you (even $5)
- Community submissions are flowing in (target: 50 games from users)

Key risks
- Model quality feels weak → be honest that v1 is descriptive-augmented, ML v2 is coming
- Nobody submits games → add a "submit and get instant analysis" hook

---

## Phase 4 — Predictive Layer + Full Product
**Weeks 23–36 · Goal: All three tiers live. Real product feel. Growing MRR.**

Deliverables
- Matchup prediction model (XGBoost or LightGBM on cumulative + community data)
- Interactive matchup explorer in the app
- Premium tier launched
- Basic user accounts (auth, personal upload history, saved lists)
- List scoring model v2 (ML-based, trained on real outcomes)
- Model card / methodology writeup — transparency builds trust
- 6+ newsletter issues shipped in this window

Exit criteria
- Free + paid + premium all live and populated
- MRR target: $200–500
- Community submissions: 500+ games in the DB

Key risks
- Model overfits early data → be strict about CV, publish uncertainty
- Feature creep → maintain a public roadmap so users see momentum without scope explosion

---

## Phase 5 — Scale & Iterate
**Month 12+ · Goal: Compound what works. Kill what doesn't.**

Focus areas
- Model retraining pipeline (weekly or event-triggered)
- Advanced features (list similarity search, meta shift detection, opponent scouting reports)
- Content deepening — tournament recap partnerships, TO collaborations
- Sponsorship / partnership talks — game stores, tournament organizers, content creators
- Consider moving off Streamlit to Next.js if UX limits are biting

---

## Cross-cutting concerns

**Legal & TOS**
- Every data source gets a `docs/data_sources.md` entry with the exact language of its terms
- Community-submitted data has clear opt-in text — users own their data, you get a license to use it in aggregate
- Don't republish another site's copyrighted content — analysis and derived stats are fine, verbatim scraped text is not

**Content cadence**
- Newsletter: biweekly minimum from Phase 2 on, weekly from Phase 4
- One post ships even when a phase slips — momentum matters more than perfection

**Metrics to track from day one**
- Newsletter subscribers
- Community-submitted games
- Repo stars + notebook views (proxy for reach)
- From Phase 3: paid conversions, MRR, churn

**Definition of Done for every phase**
- Code is on `main`, tests pass
- Deliverables listed above exist and are linked from the README
- At least one public artifact went out (post, notebook, newsletter, app update)
- `CHANGELOG.md` updated

---

## Honest bandwidth flag
Roadmap doc has this project at 1 hr/week. What's above is real software. Realistic outcomes at that pace:
- Phase 0–1: on schedule (Weeks 1–8)
- Phase 2: likely slips to Month 4–5
- Phase 3 revenue: Month 6–7, not Month 4
- Phase 4 full stack: Month 10–12

Options: accept the slip, reallocate hours from another track once ZC-MDM content is on rails, or bring in a collaborator for scraper maintenance. Decision doesn't need to be made now — just seen clearly.

---

## Deployment topology

Rule of thumb: purpose-built services for the product, one general host for the marketing surface. Don't run everything on one VPS — that's a Phase 5 problem, not a Phase 1 decision.

### Component stack

| Component | Tool (v1) | Cost | Upgrade trigger |
|---|---|---|---|
| Marketing / landing site | Hostinger (WordPress or static) | ~$3/mo | Rarely — scales fine |
| Streamlit app | Streamlit Community Cloud | Free | Sleep-on-idle hurts users, or >1 GB RAM needed |
| Streamlit app (v2) | Railway or Render | $5–10/mo | Traffic climbs, need custom domain / always-on |
| Newsletter | Substack or Beehiiv | Free tier | Want more paid-tier features or better analytics |
| Database | SQLite (in repo) | Free | Concurrent writes, community submissions arriving |
| Database (v2) | Supabase or Neon Postgres | Free tier | Free tier limits hit |
| Scrapers / cron | GitHub Actions | Free (public repo) | Runs >30 min or need persistent state |
| Scrapers (v2) | Railway worker | ~$5/mo | GH Actions timeouts biting |
| Auth + payments | Patreon | Platform fee | Want to own the customer + churn data |
| Auth + payments (v2) | Stripe + Supabase auth | 2.9% + $0.30/txn | Proven product-market fit, higher margin needed |
| Version control + CI | GitHub + GitHub Actions | Free | Never — this is the answer |

### Mental model

```
        [Data sources: Longshanks, BCP, YouTube, community]
                            ↓
              [Scrapers + cron — GitHub Actions]
                            ↓
              [Database — SQLite → Supabase]
                            ↑↓
              [Streamlit app — Cloud → Railway]
                            ↕
[Landing site — Hostinger] ←→ [Newsletter — Substack/Beehiiv]
                            ↓
                    [Newsletter subscribers]
                            ↓
                    [Patreon / Stripe]
```

### Phase-by-phase deployment reality

- **Phase 0–1** — GitHub repo only. Nothing deployed. Notebooks + local CSV.
- **Phase 2** — Newsletter live on Substack/Beehiiv. Landing page optional.
- **Phase 3** — Streamlit app deployed to Community Cloud. Landing page live on Hostinger. Patreon connected.
- **Phase 4** — Database moves to Supabase. Auth added if needed. Evaluate Railway upgrade for app.
- **Phase 5** — Custom domain, potentially Railway/Render for app, evaluate Stripe over Patreon.

### Cost trajectory

- Phase 0–2: **$0/mo**
- Phase 3: **~$3/mo** (Hostinger landing only)
- Phase 4: **~$10–15/mo** (Railway or paid Beehiiv when justified)
- Phase 5+: **~$30–50/mo** (custom domain, managed DB, worker, better hosting)

Revenue should cover cost from Phase 3 forward if the paid tier works at all. If it doesn't cover cost, that's a real signal to revisit — not a reason to keep spending.

---

## Delivery cycle per feature

The phase structure above is the macro. This is the micro — every meaningful change (a new scraper, a schema update, a new page in the app) moves through these six stages. At solo scale they shrink from weeks to minutes, but skipping them is how projects rot.

**1. Intake** — Add to `backlog.md` or GitHub Issues with a one-line description. No idea skips this step; without it, "wouldn't it be cool if" thoughts will destroy scope.

**2. Analysis** — Answer three questions in writing: Worth building? What's the smallest useful version? What does it depend on? Mark priority (P0/P1/P2). Kill or defer if the answer is soft.

**3. Build** — Create a branch (`feat/xyz` or `fix/xyz`). Commit often with real messages. Never commit straight to `main` after Phase 1.

**4. Testing** — Unit tests where they matter (data pipeline, models, anything with rules). Manual walk-through of the feature. If user-facing, get 1–2 people to try before public launch.

**5. Promotion** — 24-hour self code review with fresh eyes. Open PR to yourself. Update docs (README, `/docs`, notebook markdown). Update `CHANGELOG.md`. Merge.

**6. Hypercare** — Watch it for one week. Fix bugs before adding new features. Rule: no new work if there's a broken thing.

**Recurring themes (apply always):**
- Documentation — future-you insurance and the portfolio artifact
- Shared knowledge base — `/docs` folder grows with every feature
- Peer review — 24hr self-review + community feedback loops replace a code review team
- Business demos — screenshots on LinkedIn, dev logs in the newsletter, showing the work replaces stakeholder meetings

---

## Phase 0 execution checklist

Everything to get done before Phase 1 begins. Grouped so you can tackle one block per session. Check items off in the doc as you go — this is your Definition of Done for Phase 0.

### A. Local environment (Session 1, ~45 min) ✅ COMPLETE
- [x] Git installed and configured (`git config --global user.name` + `user.email`) — Git 2.46
- [x] Python 3.11+ installed (check with `python --version`) — *3.10.4 accepted; upgrade optional later*
- [x] `uv` installed for dependency management — 0.12.x
- [x] Editor set up — PyCharm
- [~] GitHub account exists and CLI (`gh`) is authenticated — *account exists; `gh` CLI not installed, using web UI + HTTPS clone instead (fine for now)*

### B. Repository scaffolding (Session 1, ~30 min) ✅ COMPLETE
- [x] New public repo created: `swlegion-meta`
- [x] Cloned locally to `Documents\Projects\swlegion-meta`
- [x] `.gitignore` added (Python template + project-specific rules for `data/`, `.env`, `.ipynb_checkpoints/`, `.idea/`)
- [x] Folder structure created: `/data`, `/data/raw`, `/notebooks`, `/scripts`, `/app`, `/docs`, `/tests`, `/schemas`
- [x] `.gitkeep` files added inside empty folders so Git tracks them
- [x] `data/raw/` added to `.gitignore`
- [x] `.env.example` created (empty, for future secrets); `.env` added to `.gitignore` — *completed at start of Group C*
- [x] `LICENSE` added (MIT)
- [x] `README.md` drafted with project vision, tiers, tech stack, folder map
- [x] Initial commit + push to `main` — 2 commits live

### C. Dependency + tooling setup (Session 2, ~45 min) ✅ COMPLETE
- [x] `uv init` run — project has a `pyproject.toml`
- [x] Core deps added: `pandas`, `numpy`, `jupyter`, `matplotlib`, `seaborn`
- [x] Dev deps added: `ruff` (linter/formatter), `pytest`
- [x] Virtualenv activates cleanly and Python resolves to the project env — PyCharm pointed at `.venv/`
- [x] `.python-version` file present (created automatically by `uv init`)

### D. CI pipeline (Session 2, ~30 min) ✅ COMPLETE
- [x] `.github/workflows/ci.yml` created — runs on push to any branch
- [x] Workflow steps: checkout, install uv, set up Python, `uv sync`, `ruff check`, `pytest`
- [x] `tests/test_smoke.py` added with smoke test + imports test (2 tests passing)
- [x] Pushed and CI runs green on GitHub
- [x] Green badge added to `README.md`
- [x] First lint error caught and fixed (`I001` import sorting) — good sign the pipeline actually works

### E. Data source dossier (Session 3, ~60 min) ✅ COMPLETE
- [x] `docs/data_sources.md` created (Day 2)
- [x] **Longshanks:** primary target; public data surface documented; partnership outreach identified as unlock (Group F)
- [x] **Best Coast Pairings:** deprioritized — Longshanks dominates for Legion specifically; weak stats offering
- [x] **Tabletop Admiral:** structural role identified — its JSON = Longshanks-accepted format; align schema in Group I
- [x] **Legion List Builder** (new find: LegionHQ was sunset, LLB is the replacement) — same treatment as TA
- [x] **The Fifth Trooper:** confirmed as consumer of Longshanks, not source; benchmark not competitor
- [x] **Reddit r/StarWarsLegion:** *not viable as data source* — 2026 API terms preclude commercial use; distribution channel only
- [x] **YouTube batrep channels:** Phase 5+ enrichment source via `youtube-transcript-api`
- [x] **AMG official channels:** metadata source for game state tracking
- [x] **Facebook groups:** distribution only
- [x] Each source scored 1–5 on volume, legality, effort, reliability
- [x] Sources ranked; contingency plan by Longshanks response documented

### F. Longshanks outreach (Session 3, ~30 min) 🟡 DRAFTED (v2), PENDING SEND
- [x] Contact method identified — TBD, needs current-channel verification before send
- [x] Draft email written — see `docs/longshanks_email_draft.md` (v2, reframed after Day 2 discovery that Longshanks has richer analytics than initially assessed; positioning shifted from "games Longshanks doesn't track" to "prescriptive + predictive + personal-longitudinal layer on top of their descriptive picture")
- [ ] Personalized with faction/region/competitive context
- [ ] Email sent
- [ ] Date sent logged in `docs/data_sources.md`
- [ ] Calendar reminder set for 2-week follow-up if no reply

### G. Legal + data usage alignment (Session 4, ~45 min) ✅ COMPLETE
- [x] `docs/data_usage.md` created (Day 2)
- [x] Longshanks TOS read documented — automated fetching likely violates terms; partnership is only clean path
- [x] Tabletop Admiral / Legion List Builder read — user-pasted URL parsing acceptable; automated bulk fetch is not
- [x] BCP, Reddit, YouTube, AMG reads documented
- [x] Community submission consent language drafted — grants, restrictions, user rights, retention, modification policy
- [x] Disclaimers prominent: not legal advice; lawyer review required before Phase 3 launch and any commercial partnership
- [x] "When to escalate to legal" section captures triggers (paid tier launch, partnerships, disputes, GDPR/CCPA)

### H. Vision + product brief (Session 4, ~30 min) ✅ COMPLETE
- [x] `docs/vision.md` created (Day 2)
- [x] One paragraph: what this is and who it's for — primary + secondary persona
- [x] Three tiers described with example content per tier — Free / $10 / $20 (Premium → $25–30 in Phase 5+)
- [x] Non-goals section: what this is NOT — 5 non-goals locked, news deferred
- [x] Success metrics: dual targets (floor + stretch) across subs, MRR, submissions
- [x] Bonus: cost/margin discipline, OAuth aspiration, RBDG separation, 4 open decisions logged

### I. Canonical schema v0 (Session 5, ~60 min) ✅ COMPLETE
- [x] `schemas/canonical_v0.py` created (Pydantic models)
- [x] `Player` — id, display name, region, faction preferences, longshanks_id
- [x] `Event` — id, name, date, location, format, ruleset_version, size, source
- [x] `ListIdentity` + `ListSnapshot` (Moxfield/Archidekt pattern — identity persists, snapshots version)
- [x] `Game` — id, event_id (nullable), round (nullable), player_a/b_id, list_a/b_snapshot_id, scenario, outcome, scores, game_type, played_at, source
- [x] `User`, `Unit`, `Upgrade` also included; enums for factions, ranks, outcomes, game types, sources
- [x] Version number + changelog at top of the file
- [x] Sanity test in `tests/test_schema.py`: represents a full Adepticon 2026 GT Round 3 game end-to-end
- [x] Design doc `docs/schema.md` explains rationale and rejected alternatives

### J. Exit criteria verification (Session 6, ~30 min) 🟡 NEARLY COMPLETE
- [x] You can explain the product in 2 minutes to a non-Legion friend (vision doc provides the script)
- [x] `docs/data_sources.md` has 2+ viable sources with a clear "start here" pick — Longshanks primary, community submissions moat
- [x] Repo is public, README loads cleanly on github.com, CI is green (with badge)
- [x] Longshanks email is sent (Track A + Track B ask, v3 draft with voice pass)
- [x] `docs/vision.md`, `docs/data_usage.md`, `schemas/canonical_v0.py` all committed
- [x] Backlog file exists — `docs/backlog.md` with ~25 items across Phase 1–5+
- [ ] Tag repo `v0.1.0-phase0-complete`
- [ ] Ship a launch post (LinkedIn or blog) — the ZC-MDM-adjacent "here's what I've been building" artifact

**When every box is checked, Phase 0 is complete.** Tag the repo `v0.1.0-phase0-complete`, write a short LinkedIn or blog post about the setup, and move to Phase 1.

*Phase 1–5 execution checklists will be added at the start of each phase, once we know what Phase 0 taught us. Trying to plan Phase 4 tasks now would be fiction.*

---

*Built with Claude · Update this roadmap as milestones are hit · Version 1.0*
