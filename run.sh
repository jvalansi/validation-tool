#!/bin/bash
# Full pipeline: refresh Reddit token, fetch, analyze.
set -e
cd "$(dirname "$0")"
export GH_TOKEN=$(grep -oP '^GH_TOKEN=\K\S+' /home/ubuntu/.env)
/home/ubuntu/miniconda3/bin/python ../reddit-tool/refresh_token.py
python3 fetch.py
python3 analyze.py
