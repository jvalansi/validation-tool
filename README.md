# validation-tool

Multi-source project idea validator. Gathers market signals from HN, Google Trends, Reddit, and Product Hunt, then uses Claude to produce a revenue and ROI assessment.

## Tools

### `validation_tool.py`

Searches market signals and produces a validation report.

```bash
# Single source searches
python validation_tool.py hn --query QUERY [--limit N]
python validation_tool.py trends --query QUERY [--timeframe "today 12-m"]
python validation_tool.py reddit --query QUERY [--subreddits r/sub1,r/sub2] [--limit N]
python validation_tool.py producthunt --query QUERY [--limit N]

# Full report (all sources + Claude analysis)
python validation_tool.py report --query QUERY \
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
    "signal_count": 3,
    "verdict": "validate further | weak signal — reconsider or reframe"
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
| `value` | number | Estimated realistic annual revenue ($) at 1–5% market penetration |
| `value_reasoning` | text | Explanation of value estimate |
| `suggested_probability` | number | Success probability (fixed tiers: 0.01 / 0.10 / 0.99) |
| `probability_reasoning` | text | Explanation of probability choice |

**`suggested_probability`** tiers:
- `0.01` — moonshot: weak signals, crowded market, no clear moat
- `0.10` — challenge: real demand, significant competition or execution risk
- `0.99` — sure thing: exceptional signal, clear unmet need, little competition

**`Suggested Value ($)`** = `value` (Claude's direct estimate, not a formula).

---

### `notion_validate.py`

Runs validation for a single Notion project page and writes results back.

```bash
export NOTION_TOKEN=...
python notion_validate.py <page-id> [--dry-run]
```

Reads from the page:
- `Validation Query` — product-side search query
- `Pain/Desire` — demand-side search query (triggers `--assume-tech-exists` mode)

Writes numeric/select fields to the **table**:
| Column | Source |
|---|---|
| `Probability` | Claude (`suggested_probability`) |
| `Suggested Probability` | Claude (`suggested_probability`) |
| `Value ($)` | Claude (`value` — annual revenue estimate) |
| `Suggested Value ($)` | Claude (`value` — annual revenue estimate) |
| `TAM Tier` | Rule-based (`mass` / `mid` / `niche`) |
| `Market Signal` | Rule-based from signal count (≥3=strong, 1-2=moderate, 0=weak) |
| `MRR Estimate` | Revenue estimate range (`conservative – optimistic`) |
| `Pricing Recommendation` | Claude (`pricing_assessment`) |
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

### `batch_validate.py`

Validates all unvalidated projects in the Notion Projects DB (sorted by ROI desc). Tracks completed IDs in `validated_ids.json` so re-runs pick up where they left off, even as ROI sort order shifts.

```bash
export NOTION_TOKEN=...
python batch_validate.py [--limit N]   # default: 20
```

Reads from each page: `Validation Query`, `Pain/Desire`, `Subreddits`

Writes to the **table** and **page body**: same as `notion_validate.py` above.

## Setup

```bash
pip install pytrends duckduckgo-search
```

No API keys required for HN, Google Trends, or Reddit (uses DDG `site:reddit.com`).

Claude analysis requires the Claude Code CLI (`claude`) to be authenticated.

Notion integration requires `NOTION_TOKEN` env var.
