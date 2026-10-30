# Newsletter Plan

*swlegion-meta · Phase 2 deliverable planning · v0.1*

---

## Purpose

The newsletter is the free tier of the product. Three jobs, all at once:

1. **Funnel** — top of the acquisition path, converts strangers into subscribers into paying users
2. **Credibility engine** — proves the analytical quality that justifies the paid tiers
3. **Content channel** — the thing being published, on its own terms

Every decision below balances these three.

---

## Positioning

**Hybrid: analyst's notebook (main) + broader meta commentary (contextual).**

The analyst's notebook is your differentiated edge. Personal, analytical, reproducible content built on your own game logs and community submissions. Nobody else in the Legion space does this because nobody else has the data-scientist-plus-competitive-player profile.

The meta commentary layer is table stakes. Without it, meta players (secondary persona, credibility layer) don't stay subscribed. With it, but done briefly and honestly, you get their engagement without pretending you have data you don't.

**What the newsletter is NOT:**
- A replacement for The Fifth Trooper's aggregate meta analysis
- A rules resource
- Beginner tutorial content
- Casual entertainment

If it doesn't help a mid-tier competitive player think better about their next tournament, it doesn't belong.

---

## Structure — every issue

Fixed sections in fixed order. Reader knows what they're getting every time. Consistency beats variety at launch.

### 1. The Meta Read
Short. 2–3 paragraphs. What's shifting in the competitive scene. Cited from public sources: Fifth Trooper aggregates, podcast synthesis (Notorious Scoundrels), Reddit/Discord discussion patterns, your own tournament observations. Always honest about data limits.

**Anti-pattern to avoid:** pretending to have proprietary data insights here. This section synthesizes what's publicly out there and adds competent commentary. Proprietary edge lives in The Notebook.

### 2. The Notebook (main section)
The longest section. 500–800 words. A deep-dive on something from your own recent games or your teammates' consented data:
- A matchup you're studying
- A list evolution you've been iterating on
- A scenario you keep getting wrong
- A pattern from your logged games you didn't expect

This is where your data-scientist voice earns credibility. Show the reasoning, not just the conclusion. Reader learns to think like you do.

### 3. From the Data
Short. One interesting cut of your dataset, made public. A chart, a table, a two-number comparison. Rotates each issue:
- Faction win rates from your games
- Scenario-level win % breakdowns
- List-swap impact ("switching X for Y moved my win rate from A% to B% over N games")
- Deployment or objective patterns

Reusable infrastructure. Once you build the query, each issue re-runs it with fresh numbers. ~10 minutes of work per issue at steady state.

### 4. Community Corner
Short. A submitted game, question, or observation from a subscriber, addressed. Skip in early issues (no submissions yet). Introduce around Issue 4–6 as the audience grows.

### 5. What I'm Testing Next
One paragraph. Signals ongoing work, invites engagement. "Next issue I'm digging into X. If you have data on X, reply and share it." Turns readers into participants.

---

## Cadence

**Biweekly at launch.** Sustainable at 1–2 hours of project time per week. Consistent enough to build a reading habit. Two issues per month = 26 per year.

**Upgrade to weekly** once metrics prove it out. Trigger: sustained open rate above 45%, sub growth trending toward stretch targets, and you personally feeling like you have more to say than fits in biweekly.

**Anti-pattern:** don't start weekly. Missing a weekly issue looks worse than missing a biweekly one. Start where you can be reliable.

---

## Platform: Beehiiv

**Why Beehiiv over Substack:**
- Meaningfully better growth mechanics for niche newsletters starting from zero (built-in referral programs, boost network for cross-promotion, cleaner conversion analytics)
- Free tier covers ~2,500 subscribers, more than enough through Floor and Stretch targets at Month 12
- Segmentation and upgrade path tooling that pays off when paid tier launches

**Trade-off acknowledged:** Beehiiv has more UI complexity than Substack. Substack's "write, hit publish, done" simplicity is real. For a data-scientist mindset (comfortable with tools that reward configuration), Beehiiv is the right trade. If it becomes friction, migration is possible.

**Custom domain deferred to Phase 3.** Beehiiv's default `[projectname].beehiiv.com` works at launch; custom domain when the public brand is chosen.

---

## Voice

**Blend: analytical substance, conversational voice.** Data scientist who plays competitively, written like a knowledgeable friend at the shop who happens to speak fluent regression.

Rules baked in:
- Contractions are fine, encouraged
- Sentences vary in length. Short ones matter. Long ones let you explain a mechanism when it's worth explaining.
- Data presented with what it means, not just what it says. "45% win rate, which is worse than random against this matchup, and worth understanding why" — never just "45% win rate"
- Uncertainty stated plainly. "I don't have enough games to be sure yet" beats "further analysis is warranted"
- You have opinions. Share them. "I think Krennic is undertiered, here's why"
- No corporate-speak, no thought-leader phrases, no "at the end of the day"

---

## Data foundation

**The Notebook and From the Data:** your ~350-game seed dataset from personal Longshanks history + consented teammate data, growing with community submissions over time.

**The Meta Read:** publicly cited sources:
- Fifth Trooper's aggregate stats (cite every time)
- Notorious Scoundrels and other podcasts (paraphrase and cite)
- Reddit r/StarWarsLegion discussion patterns
- Direct tournament attendance and observation

**Ruleset versioning is critical.** Every data point in From the Data or referenced in The Notebook must be tagged with the ruleset it was played under. Mixing pre- and post-balance-patch games without noting it is a credibility killer.

---

## Paid tier promotion strategy (phased)

| Issues | Strategy | Example |
|---|---|---|
| 1–3 | No paid mentions | Deliver value, build reading habit |
| 4–6 | Soft footer only | "This newsletter is the free tier of a larger project I'm building for competitive Legion players. Paid tools launching later this year." |
| 7+ | Feature previews in relevant sections | "The matchup planner I'm building would have flagged this before I played it — more on that soon" |
| Paid launch | Direct CTA in the launch issue | Dedicated section: "The tools are live" with pricing and link |
| Post-launch | Subtle mentions when topically relevant | Not every issue, only when it fits |

**Guiding principle:** every mention has to serve the reader first. Never insert a CTA that doesn't earn its place in the content around it.

---

## Distribution plan

**Launch channels (Phase 2):**
- Reddit r/StarWarsLegion — post the launch issue with genuine context, not spam-tone
- Competitive Legion Discord servers — announce in appropriate channels only, follow each server's promotion rules
- Facebook competitive Legion groups — same

**Growth mechanics (Phase 3+):**
- Beehiiv referral program — reward subscribers who bring in others (free premium month, etc.)
- Cross-promotion with adjacent Legion creators (podcasts, YouTube channels) via Beehiiv boost network
- Own-audience mentions once the paid app is live and drives its own traffic to the newsletter

**Not launching via:**
- RBDG streams or channels (personal project, keep separate)
- Paid advertising (never at these margins)

---

## Success metrics

**Floor (must-hit gate):**
- Month 6: 200 subscribers, 40%+ open rate on recent issues, sustained biweekly cadence
- Month 12: 1,000 subscribers, 35%+ open rate, weekly cadence in place

**Stretch:**
- Month 6: 500 subscribers, 45%+ open rate
- Month 12: 2,000 subscribers, 40%+ open rate

**Diagnostic signals to watch:**
- Reply rate to "reply and share your data" prompts (measures engagement, not just readership)
- Community submission rate correlated to newsletter issue drops (measures conversion to product engagement)
- Unsubscribe rate per issue (high unsub after a specific issue = signal about what didn't land)

---

## Production workflow — ~4 hours per issue at steady state

1. **Query the data** (30 min) — pull the From the Data numbers, identify a Notebook topic worth writing about
2. **Meta Read scan** (30 min) — review the last two weeks of Fifth Trooper posts, top 3 podcast episodes, r/StarWarsLegion top posts. Synthesize into 2–3 paragraphs.
3. **Notebook writing** (90 min) — the main piece. This is the section that earns credibility, so time it deserves.
4. **From the Data caption** (15 min) — one paragraph interpreting the chart, why it matters
5. **Community Corner** (15 min, when applicable) — pull one subscriber question or submission, respond
6. **What I'm Testing Next** (10 min) — one paragraph on the next issue's focus
7. **Editing pass, subject line, preheader** (30 min) — read it aloud, cut what doesn't need to be there
8. **Beehiiv setup, image, publish** (20 min) — mechanics

**First few issues will take longer** (5–7 hours) while the muscle builds. Steady state by Issue 4–5.

---

## First 6 issue topic ideas

Loose, will evolve, but these are candidate anchors so you're not starting from zero each issue:

1. **Issue 1 — Launch.** Introduction to the project, one surprising finding from your 125-game dataset that anchors the whole newsletter's thesis.
2. **Issue 2 — Matchup deep-dive** on your most-played faction vs its hardest matchup, from your data.
3. **Issue 3 — Scenario impact.** Which scenarios in the current ruleset are most one-sided, from your data + aggregate community coverage.
4. **Issue 4 — List evolution case study.** Walk through one list you've iterated on across 20+ games, what changed and why.
5. **Issue 5 — Rules change post-mortem.** How the meta shifted after the most recent balance update, using your pre/post data.
6. **Issue 6 — Reader submissions roundup.** First Community Corner as a featured section, first soft footer mention of paid tier.

---

## Open items to resolve before launch

- **Public brand name** — blocking, decides newsletter title
- **Beehiiv subscription tier configuration** — free-only for launch, paid tier config when Phase 3 approaches
- **Newsletter title style** — every issue titled "Issue 12: [Topic]" vs distinctive per-issue titles. Recommend distinctive titles for discovery, with issue number in the preheader.
- **Sender identity** — from Justin personally, or from the (yet-unnamed) product brand. Recommend personal at first (higher trust in a niche community), transition to brand-mixed once brand exists.

---

*Version history*
- v0.1 · Day 3 of Phase 0 — initial plan drafted from elicitation, ready for Phase 2 execution
