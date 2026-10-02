#!/bin/bash
# Full sweep: fetch + analyze every niche, rank, validate the top, push reports.
cd "$(dirname "$0")"
export GH_TOKEN=$(grep -oP '^GH_TOKEN=\K\S+' /home/ubuntu/.env)
/home/ubuntu/validation-tool/.venv/bin/python sweep.py "$@"
git add reports && git commit -qm "Sweep reports $(date +%F)

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>" -- reports && git push -q https://$GH_TOKEN@github.com/jvalansi/validation-tool.git HEAD:main
