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
- **Personal analytics — the tool for games Longshanks doesn't track.** Longshanks covers rated tournaments (~5–10% of a competitive player's total games). We cover the rest: casual games at the shop, practice sessions, unrated leagues, playtest games while tuning a list. Users log games via list URLs from Tabletop Admiral / Legion List Builder plus scenario data. In return, they get personal meta stats ("you win 34% vs CIS, 61% vs Rebels"), objective-by-objective breakdowns, matchup notes searchable by opponent list or archetype, and *trend analysis over time* — "your win rate improved from 45% to 58% since you swapped Grievous for Dooku." No dual entry with Longshanks; complementary coverage.
- **Community data flywheel** — anonymized submissions improve models, which improve analysis for all premium users

---

## Non-goals

Explicit list of what this is NOT — protects against scope creep as good ideas surface:

- **Beginner tutorial content** — this assumes tournament interest and existing game familiarity
- **List construction** — we consume list URLs from Tabletop Admiral / Legion List Builder and parse the JSON; we never build lists ourselves. Users edit lists on those tools and re-share the URL. This discipline is what keeps us permanently on the analysis side of the line.
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

**Long-term aspiration (Phase 3+):**
- **Read-only OAuth sync with Tabletop Admiral and Legion List Builder.** User clicks "connect TTA" (or LLB), authorizes read-only access, and their lists appear in our product automatically. On-demand refresh + periodic scheduled poll on our side; no webhooks required from theirs. Read-only scope is deliberate — it makes the ask easier for the maintainers to grant, and it enforces our non-goal: we consume lists, we never construct them.
- **This requires their cooperation, not just our engineering.** Neither TTA nor LLB currently publishes OAuth APIs. Realizing this means outreach to their maintainers, proposing the integration, and offering to help with spec and testing. Community-tool maintainers tend to be more receptive than platform companies, but we need something to show them first — this outreach is a Phase 3–4 conversation, once we have a real product and users.
- **Interim fallback (Phase 0–2):** users paste TTA/LLB list URLs manually. The visible JSON from those URLs is parseable without automation. Higher friction, but it works and is defensible.
- **Longshanks integration is a partnership question, not a technical one.** Automated fetching of Longshanks data likely violates their TOS regardless of scale. The only clean path to importing tournament games is direct partnership (see Group F outreach). If not granted, we lean fully on user-submitted data for the "games Longshanks doesn't cover" positioning — which is 80–90% of games anyway.

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
- **TTA / LLB integration outreach.** Phase 3–4 conversation with the maintainers of Tabletop Admiral and Legion List Builder, proposing a read-only OAuth API. Requires a real product and user base first; not a Phase 0 conversation.

---

*This vision doc is a living document. Update when strategic decisions shift; log changes in the version history below.*

**Version history**
- v0.1 · Day 2 of Phase 0 — initial draft based on 5-question elicitation
