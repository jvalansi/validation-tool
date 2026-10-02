# phase0 — idea sourcing (formerly opportunity-scout)

Sweeps online communities across ~20 niches for recurring pain points, ranks them as product opportunities for a
solo builder, and runs the top ones through `../phase1` (validation_tool.py). Started as the BCI pain-point study.

- `niches/<name>.json` — audience + sources (subreddits, GitHub repos, Discourse forums, HN queries).
- `fetch.py <niche>` → `data/<niche>/raw.jsonl`. Reddit goes through [rdt-cli](https://github.com/public-clis/rdt-cli)
  (installed in `../.venv`), falling back to a DuckDuckGo `site:` search if it fails. rdt-cli needs a logged-in
  `reddit_session` cookie in `~/.config/rdt-cli/credential.json` (mode 600):
  `{"cookies": {"reddit_session": "…", "loid": "…"}, "source": "manual"}` — the values are `REDDIT_SESSION` /
  `REDDIT_LOID` in `slack-claude-bot/.env`. Anonymous requests get 403.
- `analyze.py <niche>` — Claude labels pains → clusters (with profile exclusions: Apple-related, service-heavy,
  regulated, hardware) → `reports/<niche>.md` + `data/<niche>/clusters.json`. Steps are cached.
- `sweep.py` — all niches → cross-niche ranking → validation of the top N → `reports/SWEEP.md` + Discord `#validation-tool`.
- Run: `./run.sh` (detached for a full sweep). Check: `python test_score.py`. BCI ROI study: `roi/`, `validation/`.
