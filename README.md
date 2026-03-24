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
  "sources": { "hacker_news": {}, "google_trends": {}, "reddit": {}, "product_hunt": {} },
  "revenue_estimate": {
    "tam_tier": "mass | mid | niche",
    "competitor_prices_found": [],
    "conservative_mrr": "$100–$1,000",
    "optimistic_mrr": "$2,000–$10,000"
  },
  "summary": { "positive_signals": [], "signal_count": 0, "verdict": "..." },
  "claude_analysis": {
    "tam_assessment": "...",
    "tam_customers": 500000,
    "price_per_customer_annual": 228,
    "pricing_recommendation": "$19/mo SaaS",
    "key_risks": [],
    "key_opportunities": [],
    "roi_verdict": "strong | moderate | weak | unclear",
    "roi_reasoning": "...",
    "suggested_probability": 0.01
  }
}
```

**`suggested_probability`** uses three fixed tiers:
- `0.01` — moonshot (paradigm shift required, no proven path)
- `0.10` — regular challenge (tech exists, market exists, execution risk)
- `0.99` — low-hanging fruit (clear demand, proven solution, just needs building)

**`Suggested Value ($)`** is computed as: `tam_customers × price_per_customer_annual × 10` (10× revenue multiple to estimate company value).

---

### `notion_validate.py`

Runs validation for a Notion project page and writes results back to the database.

```bash
export NOTION_TOKEN=...
python notion_validate.py <page-id> [--dry-run]
```

Reads from the page:
- `Validation Query` — product-side search query
- `Pain/Desire` — demand-side search query (used when set)

Writes back to the page:
| Column | Source |
|---|---|
| `TAM Tier` | Rule-based (Google Trends score) |
| `MRR Estimate` | Claude |
| `Pricing Recommendation` | Claude |
| `Market Signal` | Claude (`roi_verdict`) |
| `Suggested Value ($)` | Computed: TAM × price × 10 |
| `Suggested Probability` | Claude (fixed tiers: 0.01 / 0.10 / 0.99) |

## Setup

```bash
pip install pytrends duckduckgo-search
```

No API keys required for HN, Google Trends, or Reddit (uses DDG `site:reddit.com`).

Claude analysis requires the Claude Code CLI (`claude`) to be authenticated.

Notion integration requires `NOTION_TOKEN` env var.
