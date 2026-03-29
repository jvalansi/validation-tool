# Phase 2 Validation: Google Ads + Landing Page

Phase 1 (HN, Reddit, Trends, Product Hunt) measures passive signal — are people talking about this problem? Phase 2 measures active intent — are people searching for a solution and willing to give you their email?

**Trigger:** Run Phase 2 when Phase 1 returns `Market Signal = strong` or `Probability ≥ 0.10`.

**Budget:** $50–100 per project ($10–15/day for 5–7 days).

**Kill signal:** <5 signups after $100 spend → kill. 3+ pre-orders at $99 → build.

---

## Input from Notion

All inputs are already in the Projects table:

| Notion Field | Used For |
|---|---|
| `Project` | Campaign name, page title |
| `Description` | Landing page hero copy |
| `Pain/Desire` | Ad copy angle, keyword themes |
| `Validation Query` | Google Ads keyword seeds |
| `Price/Customer/yr ($)` | Pricing anchor on landing page |
| `TAM Customers` | Audience sizing for ad targeting |

---

## Steps

### 1. Landing Page

One-pager deployed to GitHub Pages (`<project>.github.io` or `jvalansi.github.io/<project>`):

- **Hero:** Problem statement (from `Pain/Desire`) + one-line solution (from `Description`)
- **CTA:** "Join the beta" → Typeform collecting name, email, monthly spend on the problem
- **Social proof:** Validation signals (HN posts, Reddit threads, existing competitors)

Template lives in `promptware` repo as a reference — parameterize with project name, copy, and form URL.

### 2. Google Ads Campaign

Structure:
- **Campaign type:** Search
- **Daily budget:** $10–15
- **Keywords:** Derived from `Validation Query` and `Pain/Desire` — problem-framing terms, not product terms
  - e.g. for Promptware: "reduce openai costs", "llm api cost optimization", "query routing llm"
- **Ad copy:**
  - Headline 1: Pain point (from `Pain/Desire`)
  - Headline 2: Solution one-liner (from `Description`)
  - Headline 3: CTA ("Join Beta — Free")
  - Description: Specifics + credibility

### 3. Measurement (Days 1–7)

Track daily via Google Ads API + Typeform API → report to Slack:

| Metric | Good signal | Kill signal |
|---|---|---|
| CTR | >2% | <0.5% |
| CPC | <$3 | >$10 |
| Signups | >1/day | 0 after day 3 |
| Spend per signup | <$20 | >$50 |

### 4. Outreach (Days 4–5)

DM/email top signups:
- "What's your monthly spend on [problem]?"
- "Would you pay $[Price/Customer/yr ÷ 12]/mo for [solution]?"
- Offer a live demo → ask for $99 pre-order

### 5. Decision (Day 7)

- **0 pre-orders** → kill, move to next project in ROI table
- **3+ pre-orders** → build MVP, skip dashboard, focus on core value
- **Weak CTR but strong comments** → reframe the problem, retry with different angle

---

## Automation Opportunities

| Step | Automatable? |
|---|---|
| Landing page deploy | Yes — GitHub Pages + parameterized template |
| Google Ads campaign creation | Yes — Google Ads API |
| Typeform creation | Yes — Typeform API |
| Daily metrics pull | Yes — Google Ads API → Slack |
| Signup monitoring | Yes — Typeform API → Slack |
| Outreach drafts | Yes — Claude generates personalised DMs from signup data |

Full automation is feasible but overkill for one project at a time. Build the template and manual process first; automate the reporting loop once the playbook is proven.

---

## Project Queue

Run projects in ROI order from the Notion Projects table. After each 7-day run, update `סטטוס` (status) to `killed` or `building`.
