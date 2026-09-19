# validation-tool

Multi-source project idea validator. Gathers market signals from HN, Google Trends, Reddit, Product Hunt, and incumbent vendors, then uses Claude to produce a revenue and ROI assessment.

## Validation Phases

- **Phase 1 — Passive signals** (`phase1/`): HN, Reddit, Google Trends, Product Hunt, incumbents → market signal + ROI score
- **Phase 2 — Active intent** ([Google Ads + Landing Page](docs/phase2.md)): paid search → clicks → email signups → pre-orders. Run when Phase 1 returns strong signal.

## Tools

### `phase1/validation_tool.py`

Searches market signals and produces a validation report.

```bash
# Single source searches
python phase1/validation_tool.py hn --query QUERY [--limit N]
python phase1/validation_tool.py trends --query QUERY [--timeframe "today 12-m"]
python phase1/validation_tool.py reddit --query QUERY [--subreddits r/sub1,r/sub2] [--limit N]
python phase1/validation_tool.py producthunt --query QUERY [--limit N]
python phase1/validation_tool.py incumbents --query QUERY [--limit N]
python phase1/validation_tool.py regulatory --query QUERY
python phase1/validation_tool.py serp --query QUERY [--limit N]

# Full report (all sources + Claude analysis)
python phase1/validation_tool.py report --query QUERY \
  [--reddit-subreddits r/sub1,r/sub2] \
  [--assume-tech-exists] \
  [--pain-query "fear of death want to live forever"]
```

**`--assume-tech-exists`** — treats the technology as already working. Excludes technical feasibility from the analysis; use when tech risk is captured separately in the probability of success.

**`--pain-query`** — used together with `--assume-tech-exists`. Replaces the product query with a pain/desire framing for all source searches (e.g. search for "fear of death" instead of "consciousness upload"). Surfaces demand-side signals rather than technology-side results.

#### Report output

```json
{
  "query": "...",
  "search_query": "...",
  "sources": {
    "google_trends": {
      "average_interest": 69,
      "trend_direction": "up | down | flat"
    },
    "hacker_news": {
      "total_results": 29,
      "top_posts": [{ "title": "...", "points": 12 }]
    },
    "reddit": {
      "total_results": 7,
      "top_posts": [{ "title": "..." }]
    },
    "product_hunt": {
      "existing_products": 5,
      "top_products": [{ "name": "..." }]
    }
  },
  "summary": {
    "positive_signals": ["active Reddit discussion", "high HN interest"],
    "negative_signals": ["funded incumbent ($50M raised)"],
    "signal_count": 3,
    "competition": "funded_incumbent | crowded | contested | none_found",
    "verdict": "validate further | crowded — ... | weak signal — reconsider or reframe"
  },
  "claude_analysis": {
    "tam_assessment": "one sentence on market size with evidence",
    "tam_customers": 500000,
    "price_per_customer_annual": 228,
    "pricing_assessment": "one sentence on pricing strategy and willingness to pay",
    "key_risks": ["crowded market", "low willingness to pay"],
    "key_opportunities": ["growing search interest", "no clear market leader"],
    "value": 1200000,
    "value_reasoning": "one sentence explaining the value estimate",
    "suggested_probability": 0.01,
    "probability_reasoning": "one sentence explaining the probability choice"
  }
}
```

**Signal inputs to Claude:**
| Field | Meaning |
|---|---|
| `google_trends.average_interest` | Search interest 0–100 over past 12 months |
| `hacker_news.total_results` | Number of HN posts matching the query |
| `reddit.total_results` | Number of Reddit threads found |
| `product_hunt.existing_products` | Number of competing products on PH |

**Claude outputs:**
| Field | Type | Meaning |
|---|---|---|
| `tam_customers` | number | Estimated addressable customer count |
| `price_per_customer_annual` | number | Estimated revenue per customer per year ($) |
| `pricing_assessment` | text | Pricing strategy and willingness to pay rationale |
| `value` | number | Full TAM potential in annual revenue ($) — `tam_customers × price_per_customer_annual`, NOT discounted for penetration |
| `value_reasoning` | text | Explanation of value estimate |
| `suggested_probability` | number | Expected fraction of total value actually captured (fixed tiers: 0.01 / 0.10 / 0.99) |
| `probability_reasoning` | text | Explanation of probability choice, including expected penetration rate |

**`suggested_probability`** encodes both execution probability and realistic market penetration. The report normalises Claude's output to exactly one of three OOM values:
- `0.01` — moonshot: paradigm shift required, or <1% realistic penetration of a niche market
- `0.10` — challenge: real demand + proven tech, but significant competition (~5–15% penetration)
- `1.0` — sure thing: clear unmet demand, proven solution, little competition (high penetration likely)

All numeric fields (`tam_customers`, `price_per_customer_annual`, `value`) are OOM-rounded to the nearest power of 10 inside the report, so callers receive canonical values directly.

**Expected value** = `Value ($) × Probability` — used directly in the `Weeks of Freedom` and `ROI` formulas.

---

### `phase1/notion_validate.py`

Runs validation for a single Notion project page and writes results back.

```bash
export NOTION_TOKEN=...
python phase1/notion_validate.py <page-id> [--dry-run]
```

Reads from the page:
- `Validation Query` — product-side search query
- `Pain/Desire` — demand-side search query (triggers `--assume-tech-exists` mode)

Writes numeric/select fields to the **table**:
| Column | Source |
|---|---|
| `Probability` | Claude (`suggested_probability`) |
| `Value ($)` | Claude (`value` — annual revenue estimate) |
| `TAM Tier` | Rule-based (`mass` / `mid` / `niche`) |
| `Market Signal` | Rule-based from signal count (≥3=strong, 1-2=moderate, 0=weak) |
| `Trends Interest` | Google Trends 12-month average interest (0–100) |
| `HN Results` | Total Hacker News posts matching the query |
| `Reddit Results` | Total Reddit threads found |
| `PH Products` | Number of existing Product Hunt products found |
| `TAM Customers` | Claude's estimated addressable customer count |
| `Price/Customer/yr ($)` | Claude's estimated annual revenue per customer |

Writes text fields to the **page body** (Validation section):
- Signal counts: Google Trends avg, HN results, Reddit results, PH competitors
- Verdict callout with probability
- 🎲 Probability reasoning (quote)
- 💰 Value reasoning (quote)
- TAM assessment paragraph
- TAM customer count and price per customer per year
- Pricing assessment
- ⚠️ Key risks (bulleted)
- ✅ Key opportunities (bulleted)

---

### `phase1/notion_create.py`

**Full pipeline**: takes a raw idea and does everything end-to-end — Claude generates queries and work plan, validation tool fetches signals, Notion page is created with all fields and body filled.

```bash
export NOTION_TOKEN=...
python phase1/notion_create.py "My Project" "A system that does X for Y customers"
python phase1/notion_create.py --name "My Project" --idea "..." [--dry-run]
```

Pipeline steps:
1. Claude generates `validation_query`, `trends_query`, `pain_desire`, `work_weeks`, `description`, `target_customer`, `what_it_is`, `work_plan`
2. Runs `validation_tool.py report` with those queries (numbers are OOM-rounded and probability mapped inside the report)
3. Creates Notion page with all properties + body sections (What It Is, Target Customer, Validation Signals, Key Risks, Opportunities, Work Plan)

---

### `phase1/batch_validate.py`

Validates all unvalidated projects in the Notion Projects DB (sorted by ROI desc). Tracks completed IDs in `validated_ids.json` so re-runs pick up where they left off, even as ROI sort order shifts.

```bash
export NOTION_TOKEN=...
python phase1/batch_validate.py [--limit N]   # default: 20
```

Reads from each page: `Validation Query`, `Pain/Desire`, `Subreddits`

Writes to the **table** and **page body**: same as `notion_validate.py` above.

## Phase 2

See [docs/phase2.md](docs/phase2.md) for the full playbook. Quick start:

```bash
bash phase2/setup.sh                                    # one-time setup
python -m phase2.cli <notion-page-id> [--dry-run]       # launch campaign
python -m phase2.cli monitor [--dry-run]                # check signups
```

---

## Resources

- **Notion Projects DB** — https://notion.so/17731083-1fdd-4c06-a3c3-c87aa758703a — project ideas with validation scores, ROI estimates, and work plans
- **Validation campaigns** — https://drive.google.com/drive/u/0/folders/1qwD7Nv1MWRv3H8ZeUPqfjMnX8VZTPTVH — Google Ads campaigns, validation form, and form responses per project

## Setup

```bash
pip install pytrends ddgs
```

No API keys required for HN, Google Trends, or Reddit (uses DDG `site:reddit.com`).

Claude analysis requires the Claude Code CLI (`claude`) to be authenticated.

Notion integration requires `NOTION_TOKEN` env var.

## Incumbent detection

Product Hunt indexes *launches*. A company that launched years ago and now owns the
market never appears there — so "no PH solutions yet" used to score as an untapped
gap. Property tax appeals passed that way while Ownwell ($50M Series B, Feb 2026)
and several flat-fee vendors were actively selling.

`incumbents` probes pricing pages and funding news instead, and feeds
`summary.competition`:

| Level | Condition | Effect on verdict |
|---|---|---|
| `funded_incumbent` | any vendor raised >= $10M | verdict is "crowded", regardless of signal count |
| `crowded` | >= 5 vendors selling | verdict is "crowded" |
| `contested` | 1-4 vendors, none funded | +1 positive signal - demand proven, room to differentiate |
| `none_found` | no vendors selling | negative signal, not a gap - demand unproven or query too abstract |

Absence of competitors is never scored as upside.

**Known noise:** review and personal-finance sites (Business Insider, wallethacks)
can land in `operators`, inflating `operators_found` toward a false `crowded`.
Check the `operators` list before trusting that level; `max_funding_usd` is the
more reliable signal.

Run the checks (no network needed):

```bash
python phase1/test_validation_tool.py
```

## Kill-order checks

Phase 1 runs the cheap killers before anything is spent, in the order that a
wrong answer costs least to discover:

| # | Check | Source | Output |
|---|---|---|---|
| 1 | Are you allowed to sell it? | `regulatory` | `sources.regulatory.status`, `claude_analysis.legal_status` |
| 2 | Who already sells it, and what did they raise? | `incumbents` | `summary.competition` |
| 3 | Does one customer clear the acquisition floor? | `revenue_estimate` | `below_acquisition_floor` |
| 4 | Who owns the buyer-intent results page? | `serp` | `sources.serp_ownership.read` |

Step 5 of the method — five conversations with people who have the problem —
is deliberately not automated.

### Unit economics (step 3)

Revenue comes from an **observed competitor price**, never from search volume.
`price_is_recurring` records whether the source actually said per-month or
per-year; a bare `$49` is treated as one-time, because AppealDesk's $49 flat fee
annualized to `$49/mo` overstates revenue 12x. With no price observed, the
revenue fields are left null rather than inferred.

`ev_per_customer_annual_usd` below `MIN_EV_PER_CUSTOMER_USD` ($200) forces an
"unviable" verdict — but only with 2+ price observations, since a single scraped
number is too thin to kill an idea on.

The customer counts behind `conservative_mrr` / `optimistic_mrr` are still
assumptions, and labelled as such in `note`. The price is the only observation.

### Regulatory (step 1)

Advisory, never a verdict. A hit means "read the statute", not "stop" — the same
idea can be legal in one state and barred in another. Property tax appeals returns
the Illinois PTAB rule barring non-attorney representation, while California does
not regulate agents at all.

A hit requires both a restriction phrase and a distinctive query word, so generic
state-bar boilerplate does not flag every idea. DuckDuckGo results vary between
runs; a clean result is weak evidence, and `search_failed` marks the case where
every probe errored so that silence is never read as clearance.
