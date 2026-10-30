# Sample Newsletter Issue 1

*swlegion-meta · Content mockup for Phase 2 planning · v0.1*

*This is a sample of what a real Issue 1 could look like once the newsletter launches in Phase 2. The specifics (the "125 games" data, the deployment finding, the numbers) are illustrative — plug in real data when you write the actual issue. What's more useful here is the shape, voice, and flow.*

*This draft deliberately follows all the plan doc's structural and voice rules. It's paid-mention-free (Issue 1 in the phased strategy). Skim to feel the format, then react to what lands and what doesn't.*

---

## Draft

**Subject line:** The one deployment I've been losing at, and didn't notice for two years

**Preheader:** Issue 1 · What 125 tournament games taught me about knowing yourself

---

Hey,

I'm Justin. I play competitive Star Wars: Legion, I work in data science, and I've been logging every tournament game I've played since September 2023. That's 125 games as of this week. I finally sat down and analyzed them properly, and I found something I wasn't expecting.

This is Issue 1 of a newsletter I'm starting for mid-tier competitive Legion players. The premise is simple: what happens if you take your own tournament data seriously, treat it like real data, and actually look at it. Two years of my own games say the answer is "you find stuff you didn't know."

Here's what I found.

---

### The Meta Read

Before I get to my data, the current meta from what I can tell.

Fifth Trooper's most recent aggregate stats show CIS holding the top faction spot at 54% win rate, with Rebels close behind at 53%. Empire has slipped to 46% since the last balance patch, driven mostly by Krennic-led lists dropping off the top tables. Nothing dramatic — more of a slow rebalancing than a meta shakeup.

The podcast circuit (Notorious Scoundrels covered this well in their late-July episode) is talking a lot about Grievous droid swarms as the list to beat right now. Not because they win the most, but because they force opponents into specific tactical patterns that most lists aren't built to handle.

On r/StarWarsLegion the discussion has been quieter than usual on meta topics, more focused on the recent product releases. Take that as you will.

None of this is a surprise if you've been following the scene. It's the baseline I'm writing against.

---

### The Notebook

Here's what I found when I actually looked at my 125 games.

I break down every game by scenario — objective, deployment, and condition. I've done this since I started logging, but I never really cross-cut the data properly until this month. When I did, one number jumped out.

My win rate on **Advanced Positions deployment** is 38% across 24 games.

For context, my overall win rate across all games is 54%. My worst faction matchup is CIS at 34%. So Advanced Positions is functionally as bad as my worst faction matchup, and I didn't notice for two years because I was tracking faction data but not deployment data.

Twenty-four games isn't a huge sample, but it's not nothing. And more importantly, I checked the other deployments to make sure this wasn't just noise. Battle Lines: 58%. Danger Close: 62%. Disarray: 51%. Advanced Positions is a clear outlier.

Why is this happening? Once I saw the number, the pattern was obvious in retrospect. I run gunline lists most of the time. Advanced Positions gives your opponent a forward-deployment mechanic that lets fast units close the range gap on Turn 1. My whole plan relies on setting up firing lanes and forcing the opponent to walk into them. Advanced Positions lets them not walk.

The uncomfortable part is that I had this data the whole time. I just wasn't looking at it in a way that would surface the pattern. I was looking at faction matchups (where I was doing fine on average) and scenario objectives (where I was doing fine on average). Cross-cutting by deployment specifically wasn't something I thought to do until I was building tooling that would do it automatically.

That's the whole thesis of this newsletter, really. Personal data on your own play is full of these findings, and most competitive players never see them because logging in a spreadsheet is enough friction that we don't cross-cut the data thoughtfully.

What I'm changing based on this: I'm bringing a more flexible list to any event where I know Advanced Positions is in the deployment pool. I'm also going to log deployments as separate variables going forward instead of bundling them into "scenario" as a single field, so I can watch this pattern over time.

Two-year lesson: the numbers you don't cut aren't the numbers you don't have. They're just the numbers you haven't asked yet.

---

### From the Data

**My win rate by deployment, across 125 games (Sep 2023 — Aug 2026):**

| Deployment | Games | Win Rate |
|---|---:|---:|
| Danger Close | 27 | 62% |
| Battle Lines | 41 | 58% |
| Disarray | 33 | 51% |
| Advanced Positions | 24 | 38% |

*Filtered to games played under the current ruleset (v2.6+). Pre-v2.6 games excluded to avoid mixing eras. Full dataset is 125 games; this table represents 125 games all under current rules.*

The gap between Danger Close (62%) and Advanced Positions (38%) is 24 percentage points. If I was equally good at both, that gap should be closer to zero.

---

### What I'm Testing Next

Issue 2 (in two weeks) is going to be a matchup deep-dive on Rebels vs CIS from my data. I've logged 18 games in that matchup, which is enough to look at some real patterns. Specifically I want to figure out why my Rebels list wins against most CIS builds but loses badly to Grievous droid swarms — I have a hypothesis, and I want to check whether the data supports it.

If you have your own Rebels vs CIS games to share, hit reply. I'm not building a database yet, but I'm interested in patterns that show up across more than just my play. Especially interested in games from the last three months (post-latest-patch).

Thanks for reading Issue 1. If this was useful, forward it to a Legion player who'd get value out of it. Everything I publish is free, and probably will be for a while. If you want to see what I'm building alongside the newsletter, my code is on GitHub — [link].

See you in two weeks.

Justin

---

## Notes on this draft

**What this draft does deliberately:**

- **Opens with a specific, surprising finding**, not with "hi welcome to my newsletter." The reader learns something valuable before they know why they're reading it. The intro is embedded in the value delivery, not preceding it.
- **The Meta Read is honestly short.** Three paragraphs, all cited. Doesn't pretend to have proprietary insights.
- **The Notebook shows reasoning, not just conclusion.** The reader sees how the pattern was found and what it means, not just "here's the number." This is where credibility gets built.
- **From the Data is small but real.** One table, briefly interpreted. Every issue can have this section without heroic effort once the query pattern is built.
- **Community Corner is absent.** Issue 1 has no submissions to feature. Introduce in Issue 4–6 per the plan.
- **What I'm Testing Next primes engagement.** Reader knows what's coming, has a reason to reply, has a reason to open the next issue.
- **No paid mentions anywhere.** Issue 1 in the phased strategy. Everything is free, no CTAs, one soft mention of the GitHub as an aside.
- **Sign-off is casual, direct, human.** No "warm regards" or "stay legendary."

**Voice notes:**

- Contractions throughout ("I've been," "here's what," "you'd get")
- Mix of short and long sentences. "The gap between Danger Close (62%) and Advanced Positions (38%) is 24 percentage points." Then longer follow-up.
- Direct opinions ("The uncomfortable part is that I had this data the whole time")
- Uncertainty stated plainly ("Twenty-four games isn't a huge sample, but it's not nothing")
- No AI tells — no em dashes, no parallel triads, no "concretely," no "at the end of the day"

**What to change when you write the real Issue 1:**

- Plug in your actual surprising finding from your real 125 games. If it's not deployment-related, use whatever it actually is. The structure works for any specific-finding hook.
- Update the Meta Read with the actual current-week state of the scene when you publish
- Verify ruleset version and dates
- Your sign-off name/style
- Your GitHub link and any other identity references

**What NOT to change:**

- The structure and section order — the plan doc mandates it
- The lack of paid mentions — Issue 1 stays clean
- The voice register — this is what "analytical substance, conversational voice" looks like in practice
