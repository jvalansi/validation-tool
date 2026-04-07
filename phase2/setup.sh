#!/usr/bin/env bash
# setup_phase2.sh — one-time setup for the Phase 2 validation pipeline
set -e

PHASE2_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$PHASE2_DIR")"
PYTHON="/home/ubuntu/miniconda3/bin/python"
LOG="$PHASE2_DIR/monitor.log"

echo "=== Phase 2 Validation Pipeline Setup ==="
echo ""

# 1. Check required env vars
echo "[1/4] Checking environment variables..."
REQUIRED_VARS=(NOTION_TOKEN GH_TOKEN SLACK_BOT_TOKEN)
MISSING=()
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING+=("$var")
    fi
done
if [ ${#MISSING[@]} -gt 0 ]; then
    echo "ERROR: Missing required env vars: ${MISSING[*]}"
    echo "Set them in /home/ubuntu/slack-claude-bot/.env and re-run."
    exit 1
fi
echo "  OK"

# 2. Check service account key
echo "[2/4] Checking Google service account..."
SA_KEY="/home/ubuntu/google-service-account.json"
if [ ! -f "$SA_KEY" ]; then
    echo "ERROR: $SA_KEY not found."
    echo "Create a Google service account and download the key to $SA_KEY."
    echo "Then share your Google Sheet with the service account email."
    exit 1
fi
SA_EMAIL=$(python3 -c "import json; print(json.load(open('$SA_KEY'))['client_email'])")
echo "  Service account: $SA_EMAIL"
echo "  Make sure your Google Sheet is shared with this email (Viewer)."

# 3. Install Python dependencies
echo "[3/4] Installing Python dependencies..."
$PYTHON -m pip install cryptography --quiet
echo "  OK"

# 4. Set up cron job
echo "[4/4] Setting up daily monitor cron..."
CRON_CMD="0 7 * * * cd $REPO_DIR && $PYTHON -m phase2.cli monitor >> $LOG 2>&1"

# Remove any existing phase2 monitor cron, add new one
(crontab -l 2>/dev/null | grep -v "phase2.cli monitor"; echo "$CRON_CMD") | crontab -
echo "  Cron set: daily at 7 AM"
echo "  Log: $LOG"
echo ""

echo "=== Setup complete ==="
echo ""
echo "Usage:"
echo "  # Launch a new validation campaign:"
echo "  PYTHONPATH=$SCRIPT_DIR $PYTHON $REPO_DIR/phase2/cli.py <notion-page-id>"
echo ""
echo "  # Check active campaigns manually:"
echo "  PYTHONPATH=$SCRIPT_DIR $PYTHON $REPO_DIR/phase2/cli.py monitor"
echo ""
echo "  # Generate outreach drafts (or wait for day 5 auto-trigger):"
echo "  PYTHONPATH=$SCRIPT_DIR $PYTHON $REPO_DIR/phase2/cli.py <notion-page-id> --outreach"
echo ""
echo "  # Run day-7 decision (or wait for auto-trigger):"
echo "  PYTHONPATH=$SCRIPT_DIR $PYTHON $REPO_DIR/phase2/cli.py <notion-page-id> --decide"
echo ""
echo "The daily cron handles outreach (day 5) and kill/build decision (day 7) automatically."
