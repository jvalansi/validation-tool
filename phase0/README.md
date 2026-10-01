# phase0 — idea sourcing (formerly opportunity-scout)

Sweeps online communities across ~20 niches for recurring pain points, ranks them as product opportunities for a
solo builder, and runs the top ones through `../phase1` (validation_tool.py). Started as the BCI pain-point study.

- `niches/<name>.json` — audience + sources (subreddits, GitHub repos, Discourse forums, HN queries).
- `fetch.py <niche>` → `data/<niche>/raw.jsonl` (Reddit API, or a DuckDuckGo `site:` fallback when the API/proxy is down).
- `analyze.py <niche>` — Claude labels pains → clusters (with profile exclusions: Apple-related, service-heavy,
  regulated, hardware) → `reports/<niche>.md` + `data/<niche>/clusters.json`. Steps are cached.
- `sweep.py` — all niches → cross-niche ranking → validation of the top N → `reports/SWEEP.md` + Discord `#validation-tool`.
- Run: `./run.sh` (detached for a full sweep). Check: `python test_score.py`. BCI ROI study: `roi/`, `validation/`.
