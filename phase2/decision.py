"""
Day 7 kill/build decision logic.
Evaluates signup count and spend intent, updates Notion status, posts recommendation to Slack.
"""

import json
import os
import urllib.request
import urllib.parse

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "#proj-project-validation"
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_API = "https://api.notion.com/v1"


def _slack(text):
    if not SLACK_BOT_TOKEN:
        print(f"[Slack] {text}")
        return
    body = json.dumps({"channel": SLACK_CHANNEL, "text": text}).encode()
    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=body,
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"},
    )
    urllib.request.urlopen(req, timeout=10)


def _notion_patch(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        f"{NOTION_API}/{path}",
        data=body,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        method="PATCH",
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def run_decision(project_name, notion_page_id, pain_desire, price_per_year, dry_run=False):
    from phase2.monitor import get_formspree_responses

    responses = get_formspree_responses(project_name)
    total = len(responses)

    # Count strong signals: people who said "Around" or "More than"
    strong = sum(
        1 for r in responses
        if any(k in r.get("data", {}).get("how much would you pay for this service?", "").lower()
               for k in ["around", "more than"])
    )

    print(f"\n[Day 7 Decision] {project_name}")
    print(f"  Total signups: {total}")
    print(f"  Strong spend intent: {strong}")

    # Decision thresholds
    if strong >= 3:
        verdict = "build"
        status = "building"
        emoji = "🚀"
        reason = f"{strong} people signalled strong spend intent — enough to build."
        next_steps = "• Set up payment page\n• Schedule founder calls\n• Run outreach drafts"
    elif total >= 5:
        verdict = "validate_more"
        status = "validating"
        emoji = "🔁"
        reason = f"{total} signups but only {strong} strong spend signals — extend or pivot messaging."
        next_steps = "• Try a different headline\n• Run outreach to convert soft signals\n• Consider a price drop"
    else:
        verdict = "kill"
        status = "killed"
        emoji = "🔴"
        reason = f"Only {total} signups after 7 days — not enough signal."
        next_steps = "• Archive the landing page\n• Pick next project by ROI\n• Run `python phase2.py <next-page-id>`"

    msg = (
        f"{emoji} *{project_name} — Day 7 Decision: {verdict.upper()}*\n"
        f"{reason}\n\n"
        f"*Next steps:*\n{next_steps}"
    )

    print(f"  Verdict: {verdict} ({reason})")

    if dry_run:
        print(f"\n[dry-run] Would post to Slack:\n{msg}")
        print(f"[dry-run] Would update Notion status → {status}")
        return {"verdict": verdict, "total": total, "strong": strong}

    _slack(msg)

    # Update Notion status
    if notion_page_id and NOTION_TOKEN:
        try:
            _notion_patch(f"pages/{notion_page_id}", {
                "properties": {
                    "סטטוס": {"status": {"name": status}}
                }
            })
            print(f"  Updated Notion status → {status}")
        except Exception as e:
            print(f"  Notion update failed (status field may differ): {e}")

    return {"verdict": verdict, "total": total, "strong": strong}
