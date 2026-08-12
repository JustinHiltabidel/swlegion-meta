# Data Source Dossier

*swlegion-meta · Group E deliverable · Phase 0 · v0.1*

**Scoring rubric (1–5, higher = better):**
- **Volume** — how much relevant data exists
- **Legality** — how permissive terms are for a monetized product
- **Effort** — inverse of extraction difficulty (5 = trivial, 1 = massive)
- **Reliability** — stability of the source (5 = stable, 1 = high risk of break/change)

---

## Tier 1 — Primary sources (start here)

### 1. Longshanks (legion.longshanks.org)
**Volume: 5 · Legality: 2 · Effort: 3 · Reliability: 4**

**What it is:** The de facto tournament management platform for competitive Legion. Every rated singles event, every registration, every list submission, every game result lives here. Users can also submit casual games, log ongoing sessions, and mark data private/public.

**Public data surfaces:**
- `/events/` — future and current events with format, venue, entry
- `/results/` — global results ranked by TP (tournament points)
- `/event/{id}/` — individual events with round-by-round pairings and outcomes, battle cards (deployment/objective/condition), scores
- `/community/{id}/` — community/store pages with member game history
- Player profiles with faction preferences, event history, casual game history
- List pages (JSON-encoded lists from Tabletop Admiral / Legion List Builder)

**Analytics depth (discovered during direct exploration, Day 2):** Longshanks provides substantial descriptive analytics — faction rankings with W/L/draws and win %, battle card breakdowns (objective + secondary), advantage stats (Cunning Deployment ~46%, Advanced Intel ~61%, etc.), blue/red priority splits, game round distributions, coded list data (unit and upgrade play rates), battle card pair frequencies, trend charts over time per battle card. Some deeper features are paywalled (starred).

**Practical implication:** The descriptive layer is theirs and it's mature. Our differentiation lives cleanly in prescriptive (list scoring, matchup planning), predictive (simulation), and personal longitudinal (trend analysis tied to specific list changes) — not in trying to build a better descriptive dashboard.

**Legal status:** Terms restrict use of scraped data for external products. **Directionally, automated fetching of Longshanks data likely violates their TOS regardless of scale** — including user-triggered "paste your event URL, we fetch it" patterns. The distinction between bulk scraping and one-URL-at-a-time fetching feels meaningful in UX but isn't legally protective; both involve a system other than the browser fetching and storing platform data. **Direct partnership is the only clean path** — the site references working with community projects. Group F outreach is critical. *Not legal advice — read the actual TOS carefully in Group G; get a lawyer's read if real revenue is on the line.*

**Fallback UX patterns if partnership fails:**
- **Browser extension** — user browses their Longshanks pages normally, extension structures the page they're already viewing into your app. Cleaner because there's no server-side automation; a person is using their browser and a tool is helping them organize what they see.
- **User-exported upload** — if Longshanks offers any export (CSV, JSON, print view), user exports their own data and uploads it. Verify existence during Group F.
- **Manual entry with heavy assistance** — autocomplete from prior entries, quick-select faction/objective/deployment. Highest friction, lowest TOS exposure.

**Recommendation:** Reach out for partnership first (Group F). If granted, build sanctioned integration. If not, ship browser-extension or manual-entry patterns and lean on the prescriptive/predictive/personal-longitudinal wedges — never on trying to replicate Longshanks' descriptive analytics.

---

### 2. Community submissions (user-uploaded data)
**Volume: TBD (grows with users) · Legality: 5 · Effort: 4 · Reliability: 5**

**What it is:** Structured game data users log through your product. List URLs (from Tabletop Admiral / Legion List Builder — we never build lists ourselves), scenario (objective/deployment/condition), turn-by-turn scores, opponent info, notes.

**Positioning — prescriptive, predictive, and personal-longitudinal analytics on top of Longshanks' descriptive picture:** Longshanks provides a mature descriptive view of the meta (faction rates, battle card outcomes, coded list data, aggregate trends). What doesn't exist anywhere is personal + prescriptive analysis tied to a player's own history: "how has my Krennic list performed since I swapped Grievous for Dooku," "given my play history, what should I bring to CIS?" That's the wedge. Community submissions power it, and users log games with us because the return on investment is personal insight they can't get anywhere else.

**What the user gets back (the draw):**
- Personal meta stats — "you win 34% vs CIS, 61% vs Rebels"
- Objective-by-objective breakdown across your games
- Matchup notes searchable by opponent list or archetype
- **Trend analysis tied to specific list changes** — "your win rate improved from 45% to 58% since you swapped Grievous for Dooku"
- Prescriptive list refinement suggestions from your data + aggregate community data
- Predictive simulation of matchups you haven't played yet

None of this exists in the Legion ecosystem for the mid-tier competitive player. Longshanks gives you descriptive meta; we give you personal, prescriptive, predictive analytics.

**Scope discipline (critical):**
- We **consume** list URLs from TA / LLB; we never let users construct or edit lists in our tool
- If they want to change a list, they go back to TA / LLB, edit there, re-share the URL
- This friction is a feature — it enforces our scope permanently

**Legal status:** Fully permissible with clear consent language (defined in Group G). Users grant a license to use aggregate data for analysis and model training; they retain ownership.

**Recommendation:** Design the submission workflow into the app from Day 1. Premium tier's personal longitudinal analytics is the hook that drives submissions.

---

## Tier 2 — Structural sources (list format + integrations)

### 3. Tabletop Admiral (tabletopadmiral.com)
**Volume: N/A (structural) · Legality: 3 · Effort: 4 · Reliability: 5**

**What it is:** Dominant Legion list builder. Users create army lists here and share via URL. JSON export exists. Also supports Shatterpoint.

**Why it matters:** TA's JSON export = the format Longshanks accepts for list statistics. TA is the upstream source of structured list data flowing everywhere. Aligning your canonical schema to TA's format gives round-trip compatibility with both TA and Longshanks in one design decision.

**Long-term aspiration:** OAuth or account linking so users pull TA lists directly into your app. Phase 5+ conversation with the TA maintainer.

**Recommendation:** Group I schema alignment. Examine TA's JSON export format before finalizing canonical `List` model.

---

### 4. Legion List Builder (legionlistbuilder.com)
**Volume: N/A (structural) · Legality: 3 · Effort: 4 · Reliability: 3**

**What it is:** Community-maintained replacement for the now-sunset LegionHQ. Built on ~99% of the original codebase. Alternative to Tabletop Admiral.

**Why it matters:** Some players use LLB instead of TA. Canonical schema should accommodate lists from either source.

**Recommendation:** Same as TA — align schema, target Phase 5+ integration. Update vision doc OAuth aspiration to reference Legion List Builder instead of the sunset LegionHQ.

---

## Tier 3 — Adjacent sources (supplementary, limited use)

### 5. Best Coast Pairings (bestcoastpairings.com)
**Volume: 3 · Legality: 2 · Effort: 3 · Reliability: 3**

**What it is:** Multi-system tournament management platform. Paid subscription unlocks cross-event lists and stats.

**Legion coverage:** Present but Longshanks dominates the Legion competitive scene specifically. BCP appears more at multi-system conventions.

**Legal status:** Cross-event access behind paywall. No clear developer API. User reviews cite unreliable stats offering and mid-event software issues.

**Recommendation:** Deprioritize. Not worth the effort vs. Longshanks for Legion-specific data. Revisit only if Longshanks refuses partnership.

---

### 6. Reddit — r/StarWarsLegion
**Volume: 2 · Legality: 1 · Effort: 3 · Reliability: 2**

**Critical 2026 API changes make this unviable as a data source for a paid product:**
- Free tier requires manual approval, 2–4 week timeline
- 100 QPM for authenticated OAuth clients, **non-commercial use only**
- Commercial use requires ~$12,000/year minimum contract at $0.24/1K calls
- Unauthenticated JSON endpoints returning HTTP 403 since May 2026
- November 2025 "Responsible Builder Policy" extended pre-approval to all developers

**Implication:** Phase 0–3 personal exploration is technically fine on free tier. Phase 4+ productization is commercial use, requires enterprise contract. Not viable as a real data source.

**Better role:** Marketing / distribution channel. Post insights, engage with community, drive traffic to newsletter.

**Recommendation:** Use for distribution, never for data ingest.

---

### 7. YouTube batrep channels
**Volume: 3 · Legality: 4 · Effort: 2 · Reliability: 4**

**What it is:** Community content creators producing battle reports of tournament and high-level games. Notorious Scoundrels, various top-player channels.

**Data extraction:** Text transcripts via `youtube-transcript-api` for public videos. Legal for research use; analysis is generally fair use, verbatim redistribution is not.

**Why it matters at all:** Phase 5+ potential for enriching player/list metadata with "how did they play it, what were their key decisions."

**Recommendation:** Note as Phase 5+ enrichment source. Do not build near-term.

---

### 8. AMG / Atomic Mass Games official channels
**Volume: 2 · Legality: 5 · Effort: 5 · Reliability: 5**

**What it is:** Rules updates, unit stat changes, product releases, balance patches.

**Why it matters:** Models need to know when unit stats change or new units release. This metadata shapes every downstream analysis.

**Recommendation:** RSS or manual monitoring for release cadence. Build a lightweight `docs/game_state.md` tracking current Legion version, latest patch, unit release timeline. Not a data source in the ML sense — essential context.

---

### 9. Facebook competitive Legion groups
**Volume: 1 · Legality: 1 · Effort: 1 · Reliability: 2**

**What it is:** Discussion groups for competitive Legion players.

**Founder note:** Discussion is more philosophical/strategy than meta/matchup data. Better as a distribution channel than a data source.

**Recommendation:** Marketing channel only. Not a data source.

---

## Ranked "start here" for Phase 1 data ingest

1. **Longshanks (via partnership if possible)** — Group F outreach immediately
2. **Community submissions** — design into the product from Day 1, moat asset
3. **Tabletop Admiral schema alignment** — Group I schema decision, unlocks Longshanks compat in the same design
4. **AMG game state tracking** — lightweight, essential for model correctness

**Deferred to Phase 5+ or ruled out:**
- BCP — only if Longshanks refuses partnership and BCP proves richer than expected
- Reddit — distribution channel, never data source (2026 API terms preclude commercial use)
- YouTube transcripts — enrichment source, not core
- Facebook — distribution channel only

---

## Contingency plan by Longshanks response

**If Longshanks says YES to partnership:**
- Fast path to real data via legitimate access
- Phase 1 focuses on ingest pipeline + first newsletter
- Community submissions become a Phase 3 addition, not the primary source

**If Longshanks says NO:**
- Community submissions become the primary data source, on accelerated timeline
- Every product feature designed to encourage submissions
- Consider narrower initial scope: "analysis tool for lists you've played, using data you upload"

**If Longshanks doesn't respond within 2 weeks:**
- Send a shorter, more specific follow-up
- Proceed with community-submissions-primary plan in parallel
- Never scrape aggressively; honor `robots.txt` and rate limits religiously

---

## Open questions for next phases

- **Group F (outreach):** email tone — collaborative/co-creator framing works best. Draft together.
- **Group G (legal):** need to write consent language for community submissions and document Longshanks TOS clauses that constrain us if partnership fails.
- **Group I (schema):** examine Tabletop Admiral's JSON export format directly before finalizing schema. Round-trip compatibility with TA/Longshanks is worth designing around.

---

*This dossier is a living document. Update as source status changes.*

**Version history**
- v0.1 · Day 2 of Phase 0 — initial dossier from web research
