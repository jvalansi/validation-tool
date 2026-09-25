# bci-painpoints

Mines BCI/EEG/neural-data communities for recurring pain points and ranks them as product opportunities.

- `fetch.py` — GitHub issues (10 BCI/EEG repos, most-discussed), Reddit (r/BCI, r/OpenBCI, …, top posts), MNE Discourse → `data/raw.jsonl`
- `analyze.py` — Claude labels pains → clusters → assigns → `report.md`
- Score = count × (1 + share with paying signal) × ML fit (Claude-judged)

Run: `./run.sh` (refreshes the Reddit token via `../reddit-tool`). Check: `python3 test_score.py`.
