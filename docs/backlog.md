# Backlog

*swlegion-meta · Items surfaced during Phase 0 that don't belong in Phase 0*

Living document. Add items as they surface, reprioritize as phases progress.

---

## Phase 1 targets (immediately after Phase 0 exit)

### Data + schema
- [ ] Examine Tabletop Admiral's actual JSON export format directly — validate canonical schema alignment before real ingest (open item in `docs/schema.md`)
- [ ] Populate Unit + Upgrade reference tables from AMG published data
- [ ] Enum-ify primary missions / secondary missions / advantages in the schema — currently free-form strings, promote to enum once real data flows
- [ ] Design and build the community game submission flow (form or Streamlit MVP)
- [ ] Confirm current Legion ruleset version and replace `RULESET = "2.6"` placeholder in `tests/test_schema.py`

### Longshanks follow-up
- [ ] 2-week follow-up email if no reply from Track A / Track B outreach
- [ ] If they respond positively: sanction-specific integration design
- [ ] If they decline: browser-extension MVP design for user-driven data import
- [ ] Verify whether Longshanks offers any user-facing data export today (relevant to Track B fallback)

### Product / brand
- [ ] Decide on public product name and brand identity (blocking Phase 2 newsletter launch)
- [ ] Choose newsletter platform — Substack vs Beehiiv, final call at Phase 2 start
- [ ] Register domain once name is chosen

---

## Phase 2 targets (newsletter launch, Month 2–3)

- [ ] Landing page on Hostinger (marketing surface)
- [ ] Newsletter platform live, first 3–4 issues drafted
- [ ] Community wait-list capture form
- [ ] Basic analytics tracking (subscribers, engagement)
- [ ] Publicize project on Reddit r/StarWarsLegion, Discord servers, competitive Facebook groups

---

## Phase 3+ targets (paid tier launch)

- [ ] Legal review of Terms of Service and Privacy Policy (drafted intent lives in `docs/data_usage.md`)
- [ ] Consent flow design based on the community submission language in `docs/data_usage.md`
- [ ] Streamlit app MVP for list scorer + basic matchup planner
- [ ] Patreon or Stripe integration
- [ ] Deploy to Streamlit Community Cloud
- [ ] Onboarding flow for new users (link submissions, first-run analysis)

---

## Ideas parked (revisit periodically)

- [ ] YouTube batrep transcript extraction (Phase 5+ enrichment source)
- [ ] Tabletop Admiral / Legion List Builder OAuth outreach (Phase 3–4, after MVP exists and there's something to show them)
- [ ] Affiliate revenue via product release coverage (Phase 5+, sidebar only per vision doc)
- [ ] Team / doubles format support (schema extension)
- [ ] Multi-round tournament schema — possible `Round` entity if analysis demands it

---

## Open strategic questions

- [ ] Paid tier refinement — Longshanks descriptive depth is richer than initially assessed; matchup planner needs sharper prescriptive framing to avoid overlap (noted in `docs/vision.md`)
- [ ] Newsletter data source resolution — depends on Group F reply from Longshanks
- [ ] Public brand vs engineering repo name — `swlegion-meta` is fine for GitHub; product needs its own identity before Phase 2 launch

---

*Prioritization principle: items that unblock other items go first. Data / schema before product build; product build before marketing surface; marketing surface before paid tier.*
