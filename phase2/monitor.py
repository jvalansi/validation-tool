"""
Daily monitor for active validation campaigns.
Reads Tally form responses, computes metrics, posts summary to Slack.
"""

import json
import os
import urllib.request
from datetime import datetime, timezone

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "#proj-project-validation"
CAMPAIGNS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "campaigns.json")


def _slack(text):
    if not SLACK_BOT_TOKEN:
        print(f"[Slack] {text}")
        return
    payload = json.dumps({"channel": SLACK_CHANNEL, "text": text}).encode()
    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=payload,
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"Slack post failed: {e}")


def load_campaigns():
    if not os.path.exists(CAMPAIGNS_FILE):
        return []
    with open(CAMPAIGNS_FILE) as f:
        return json.load(f)


def save_campaigns(campaigns):
    os.makedirs(os.path.dirname(CAMPAIGNS_FILE), exist_ok=True)
    with open(CAMPAIGNS_FILE, "w") as f:
        json.dump(campaigns, f, indent=2)


def register_campaign(project_name, form_id, pages_url, days=7):
    """Called after a successful deploy to track the campaign."""
    campaigns = load_campaigns()
    # Replace existing entry for same project
    campaigns = [c for c in campaigns if c["project"] != project_name]
    campaigns.append({
        "project": project_name,
        "form_id": form_id,
        "pages_url": pages_url,
        "start_date": datetime.now(timezone.utc).isoformat(),
        "days": days,
        "status": "active",
    })
    save_campaigns(campaigns)


def days_elapsed(start_date_iso):
    start = datetime.fromisoformat(start_date_iso)
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - start).days


def run_monitor(dry_run=False):
    from phase2.forms import get_responses

    campaigns = load_campaigns()
    active = [c for c in campaigns if c.get("status") == "active"]

    if not active:
        print("No active campaigns to monitor.")
        return

    for campaign in active:
        project = campaign["project"]
        form_id = campaign["form_id"]
        pages_url = campaign["pages_url"]
        total_days = campaign.get("days", 7)
        day = days_elapsed(campaign["start_date"]) + 1

        print(f"\nChecking campaign: {project} (day {day}/{total_days})")

        try:
            responses = get_responses(form_id)
        except Exception as e:
            print(f"  Failed to fetch responses: {e}")
            responses = []

        total = len(responses)
        spend_counts = {}
        for r in responses:
            v = r.get("spend", "")
            if v:
                spend_counts[v] = spend_counts.get(v, 0) + 1

        # Projection
        pace = total / day if day > 0 else 0
        projected = int(pace * total_days)

        # Recommendation
        if day >= total_days:
            rec = "⏰ Campaign ended."
        elif projected >= 10:
            rec = "✅ Strong signal — continue"
        elif projected >= 5:
            rec = "⚠️ Moderate signal — monitor closely"
        else:
            rec = "🔴 Weak signal — consider killing"

        lines = [
            f"*{project} — Day {day}/{total_days}*",
            f"Signups: {total} total  |  Pace: {pace:.1f}/day  |  Projected: {projected}",
        ]
        if spend_counts:
            lines.append("Spend intent: " + "  |  ".join(f"{v}: {k}" for k, v in sorted(spend_counts.items(), key=lambda x: -x[1])))
        lines.append(f"Landing page: {pages_url}")
        lines.append(rec)

        msg = "\n".join(lines)
        print(msg)

        if not dry_run:
            _slack(msg)

        # Mark campaign as ended if past duration
        if day > total_days:
            campaign["status"] = "ended"

    save_campaigns(campaigns)
