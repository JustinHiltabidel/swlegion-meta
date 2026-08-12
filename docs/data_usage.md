# Data Usage & Legal Alignment

*swlegion-meta · Group G deliverable · Phase 0 · v0.1*

## Purpose

Document how we interact with each data source (what we believe we can do, what we won't) and define the terms under which community-submitted data flows through the product. This is our reference when questions come up — before a scraping decision, before shipping a consent form, before running an analysis on shared data.

---

## Critical disclaimer

**This document is our best-effort read of publicly available terms, not legal advice.** The author is not a lawyer. Before commercial launch, all consent language, terms of service, and data-use claims should be reviewed by a lawyer. Especially:

- Before revenue starts (Phase 3, paid tier launch)
- Before partnership contracts with any data provider
- If we accept EU users (GDPR) or California users (CCPA)
- If revenue crosses ~$10k/year
- If a data provider disputes our use

Living document. Update as source terms change or as legal review adds precision.

---

## Per-source read

### Longshanks (legion.longshanks.org)

**Our read:** Automated fetching of Longshanks data likely violates their terms regardless of scale. This includes bulk scraping, user-triggered server-side fetches ("paste your URL, we fetch it"), and cached mirror representations of their content.

**What we believe is acceptable:**
- Human browsing
- Users manually copying their own data into our tool (via forms or a browser extension that reads what they're already viewing)
- Partnership-granted access under whatever terms Longshanks defines

**Practical rules:**
- Do not build scrapers targeting Longshanks
- Do not build "paste URL, we fetch" import features without partnership
- Group F outreach is the only clean path to programmatic data access
- If Longshanks says no, we build browser extension or manual entry patterns instead

**Escalate to legal:** if a partnership is offered and money or ongoing obligations attach, review the contract.

---

### Tabletop Admiral (tabletopadmiral.com)

**Our read:** Users pasting their own list URLs into our tool and us parsing the visible JSON is likely acceptable — the user is voluntarily sharing their own content. Automated bulk fetching of arbitrary lists (e.g., fetching every list submitted to a Longshanks event) is a different question and we do not do it.

**What we believe is acceptable:**
- Users paste their TA list URL; we parse the JSON; we store the structure
- Users grant implicit permission to store and analyze their own lists when they submit them
- We display our own analysis of their lists back to them

**What we should avoid:**
- Automated bulk fetching of list URLs users didn't explicitly share
- Republishing verbatim list content publicly without user permission (analysis and derived stats are fine)
- Using TA's branding or claiming affiliation

**Long-term (Phase 3+):** OAuth partnership conversation with TA maintainers to formalize the integration.

**Escalate to legal:** before commercial-scale integration or any formalized partnership.

---

### Legion List Builder (legionlistbuilder.com)

**Our read:** Same as Tabletop Admiral. Community-maintained project. Same acceptable/avoid rules apply.

---

### Best Coast Pairings (bestcoastpairings.com)

**Our read:** Data behind paid subscription paywall. Deprioritized in the data dossier. If we ever ingest BCP data, we'd need a specific reason and a review of their commercial terms.

**Practical rule:** Skip for now. Revisit only if Longshanks partnership fails and BCP proves richer for Legion-specific data than currently expected.

---

### Reddit

**Our read:** Reddit's 2023 API pricing plus 2025 Responsible Builder Policy make Reddit off-limits as a data source for a commercial product. Free tier is non-commercial only; commercial use requires ~$12k/year minimum enterprise contract at $0.24 per 1K calls.

**Practical rule:** Use Reddit as a distribution channel (posts, engagement, discovery). Never as a data source in our pipeline.

---

### YouTube (batrep transcripts)

**Our read:** Transcript access via `youtube-transcript-api` is generally acceptable for public videos. Analysis of transcript content is fair use. Verbatim redistribution is not.

**Practical rules:**
- Extract and analyze transcripts for enrichment
- Quote briefly with attribution in newsletter content
- Do not republish full transcripts
- Phase 5+ enrichment source only — not core

---

### AMG official data

**Our read:** Publicly published game data (unit stats, rules, points) is fair use for analysis, reference tables, and product content.

**Practical rules:**
- Build canonical Unit and Upgrade catalogs from published AMG sources
- Credit AMG as the source of canonical game data
- Do not claim affiliation or endorsement

---

## Community submission consent — intent and structure

This section describes the intent behind the consent language we present when users submit game data. **The final legal wording should be drafted or reviewed by a lawyer before Phase 3 paid tier launch.** What follows is intent, not finished terms.

### What the user is granting us

When a user submits a game record, list URL, or other data through our product, they grant us a **non-exclusive, worldwide, royalty-free license** to:

1. **Store their data** in our systems for the duration of their account
2. **Analyze their data** to provide them personalized statistics, insights, and recommendations
3. **Aggregate their data anonymously** with other users' data to compute community-wide statistics (e.g., "faction win rates," "top-performing archetypes")
4. **Train predictive models** on aggregated data to improve product recommendations and analysis quality
5. **Publish derived statistics** in newsletters and public content — statistics only, never identifiable content (specific lists, personally identifiable information, individual game details) without explicit user permission

### What we will not do

1. **Sell or share their personal data** with third parties for marketing or unrelated commercial use
2. **Republish their specific lists** publicly without their explicit permission
3. **Expose their identity** in public content (newsletter, social media, analytics posts) without permission
4. **Retain data indefinitely after account deletion** — permanent purge within 30 days of account closure request
5. **Use their data to compete against them** in tournaments (they retain their strategic edge)

### User rights

Users can, at any time:

1. **Access** their data — download in machine-readable form
2. **Correct** their data
3. **Delete** their data — immediate soft-delete, permanent purge within 30 days
4. **Opt out of aggregate analysis** — data used only for their own personal analytics
5. **Withdraw consent to specific uses** (e.g., "no model training on my data")

### Data retention

- **Active accounts:** data retained indefinitely to power ongoing personal analytics
- **Cancelled accounts:** 30-day deletion window, then permanent purge
- **Aggregate-only opt-outs:** raw data retained for the user's own analytics; excluded from aggregate computations

### Modifications to consent

If we materially change how we use community data (new use cases, new data sharing), we will:

1. Notify all users at least 30 days before the change takes effect
2. Require explicit re-consent for uses that expand beyond original agreement
3. Log all consent changes for audit purposes

---

## When to escalate to legal review

- **Before Phase 3 launch** — any paid tier going live requires proper Terms of Service and Privacy Policy drafted by a lawyer
- **Before partnership contracts** with Longshanks, Tabletop Admiral, Legion List Builder, or other data providers
- **If a data provider disputes** our use of their data
- **Before international expansion** in ways that trigger GDPR (EU users) or CCPA (California users) — likely earlier than expected, since EU users may sign up freely
- **If we accept investment** or plan an acquisition

At Phase 0, this doc is a working intent document. At Phase 3+, it needs professional review before it becomes user-facing terms.

---

## Open items

- **Terms of Service** (user-facing) — draft with a lawyer before Phase 3
- **Privacy Policy** (user-facing) — same
- **Cookie policy** — needed if we deploy any analytics on the marketing site
- **GDPR compliance review** — before accepting EU users at scale
- **CCPA compliance review** — before accepting California users at scale (relevant even from Phase 3 since we're US-based)

---

*Version history*
- v0.1 · Day 2 of Phase 0 — initial draft; per-source reads and community submission intent
