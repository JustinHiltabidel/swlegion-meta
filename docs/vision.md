# Product Vision — swlegion-meta

*A tiered data product for the competitive Star Wars: Legion community.*

**Status:** 🚧 Phase 0 — Foundation & Discovery. Vision drafted; data source dossier and canonical schema pending.
**Version:** v0.1 · Day 2 of Phase 0

---

## What this is

A tiered data product for competitive Star Wars: Legion players. The free tier is a newsletter covering meta trends, tournament recaps, and unit-level analysis. The paid tier delivers decision-support tooling — list scoring, archetype playbooks, and matchup planning. The premium tier delivers simulation and personalized game analysis, using structured community-submitted game data as its flywheel.

The product exists to answer questions the mid-tier competitive player is already asking: *"how do I beat this heavy list?"* and *"what pairs well into this scenario?"* It differentiates from existing sources — notably The Fifth Trooper — by moving beyond descriptive meta reporting into decision-support tooling.

---

## Personas

**Primary — the mid-tier competitive player breaking into the scene.**
Plays local RTTs and regional events, has ambition to podium at bigger events, feels the gap between where they are and where top players are. Actively looks for tools to close that gap. Larger population than the meta cohort, and more sustained subscription revenue because the instructional value hits harder for them.

**Secondary — the meta / GT chaser.**
Travels to majors, deeply knowledgeable, cares about hyper-tuned edge. Small population but shows up first and is loud. Their engagement validates analytical quality; their credibility spills onto the product. Expect them to test the free tier hard and some to convert to premium for the simulator.

**Not the target user:**
- Beginners exploring the game
- Casual local league players not interested in competitive
- Non-players / spectator-only fans

---

## Value proposition per tier

**Free — the newsletter.**
Biweekly at launch, weekly by Phase 4. Meta commentary, tournament recaps, unit-level analysis, tier lists. This is the funnel and the credibility engine. Every issue proves the analytical quality that justifies the paid tiers.

**Paid ($10/mo) — decision support.**
- **List scorer** — "here's how your list stacks against the current meta, with weak spots identified"
- **Archetype playbooks** — deep guides per faction/build with unit-level reasoning
- **Basic matchup planner** — "here's how to approach List A vs List B on this objective"

**Premium ($20/mo at launch → $25–30 in Phase 5+) — full stack.**
- **Full matchup simulator** — predictive game outcome models with detailed variant analysis. *"The ability to simulate is the beast."*
- **Personal game analysis** — users submit structured game data (lists, scenario, turn-by-turn scores, notes) and receive AI-augmented coaching feedback
- **Community data flywheel** — submissions improve models, which improve analysis for all premium users

---

## Non-goals

Explicit list of what this is NOT — protects against scope creep as good ideas surface:

- **Beginner tutorial content** — this assumes tournament interest and existing game familiarity
- **List building tool from scratch** — the product analyzes lists; construction is Tabletop Admiral / Legion HQ2's job
- **Rules resource / errata reference** — AMG and official channels handle this
- **Community forum / social platform** — Discord and Reddit already own this space

**Deferred (not banned; revisit Phase 5+):**
- General Legion news / product release coverage — potential affiliate revenue path if kept sidebar and modest. Not core.

---

## Distribution + audience

**Independent from Roll Better Dice Gaming.** RBDG streaming activities are separate and remain so; this is a personal project with its own identity (public brand naming TBD).

**Launch channels:**
- Reddit — r/StarWarsLegion
- Discord — Legion-focused competitive servers
- Facebook — competitive Legion groups

**Long-term aspiration (Phase 5+):**
- OAuth integration with Tabletop Admiral and Legion HQ2 so users can pull their lists directly into the product. Would materially reduce friction and could 10x adoption if landed. Named here so early schema decisions don't preclude round-tripping with those systems.

---

## Success metrics — dual targets

**Floor (must-hit gate — if missed, diagnose):**
- Month 6: 200 subscribers · $200 MRR · 50 community submissions
- Month 12: 1,000 subscribers · $1,500 MRR · 500 community submissions

**Stretch (great execution target):**
- Month 6: 500 subscribers · $500 MRR · 100 community submissions
- Month 12: 2,000 subscribers · $2,300 MRR · 1,000 community submissions

Ambitious outcomes (5k subs, $5k+ MRR at M12) are aspirational — the project is not planned around them.

---

## Cost + margin discipline

- **Phase 0–3:** near-zero infrastructure spend. Free tiers only. Streamlit Community Cloud, Supabase free tier, GitHub Actions.
- **Phase 4+:** real AWS or managed hosting justified only when revenue covers it.
- **Target gross margin:** 70%+ from Month 6 forward.
- **Claude API costs scale with paid users, not free** — designed so the free tier can grow without proportional cost. Claude powers written analysis and coaching feedback, not the underlying simulator (which is a trained ML model).

---

## Open decisions / deferred

- **Product name and brand.** The repo is `swlegion-meta` for engineering; the public brand needs its own identity. Decide before Phase 2 (newsletter launch).
- **Newsletter platform.** Substack vs. Beehiiv — decide when nearing Phase 2. Beehiiv is stronger for growth mechanics; Substack for near-term discovery.
- **Payment platform.** Patreon vs. Stripe — Patreon for simplicity at launch; migrate to Stripe in Phase 5 if margin or data ownership pressure warrants.
- **First scraper target.** Determined by Group E (data source dossier) — likely Best Coast Pairings if Longshanks doesn't grant partnership access.

---

*This vision doc is a living document. Update when strategic decisions shift; log changes in the version history below.*

**Version history**
- v0.1 · Day 2 of Phase 0 — initial draft based on 5-question elicitation
