#!/bin/bash
# Weekly pipeline (weekly.py): new niches → sweep + phase 1 → top ideas into Notion → phase 2 launches.
# Commits and pushes the reports, niches and validation cache.
cd "$(dirname "$0")"
# Read KEY=VALUE lines literally: `source` stops at a backtick in one of the values.
while IFS='=' read -r k v; do export "$k=$v"; done < <(grep -E '^[A-Za-z_][A-Za-z0-9_]*=' /home/ubuntu/slack-claude-bot/.env)
export GH_TOKEN=$(grep -oP '^GH_TOKEN=\K\S+' /home/ubuntu/.env)
/home/ubuntu/validation-tool/.venv/bin/python weekly.py "$@"
git add reports niches validated.json && git commit -qm "Weekly sweep $(date +%F)

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>" -- reports niches validated.json && git push -q https://$GH_TOKEN@github.com/jvalansi/validation-tool.git HEAD:main
