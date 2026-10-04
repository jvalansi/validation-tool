"""
Day 7 kill/build decision logic.
Evaluates signup count and spend intent, updates Notion status, posts recommendation to Slack.
"""

import json
import os
import urllib.request
import urllib.parse

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_API = "https://api.notion.com/v1"


from .notify import post as _slack  # Discord #validation-tool


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


# ~100 clicks before any kill: at a 5% signup rate, 15 clicks still give 0 signups about half the time.
MIN_CLICKS = 100
MAX_COST_PER_SIGNUP = 50


def decide(total, strong, clicks=None, spend=None):
    """Verdict from signups, strong spend intent and, when ads ran, clicks and spend."""
    if strong >= 3:
        return "build"
    if clicks is None:  # no ad data: fall back to raw signup count
        return "validate_more" if total >= 5 else "kill"
    if clicks < MIN_CLICKS:
        return "extend"
    if total and spend / total <= MAX_COST_PER_SIGNUP:
        return "validate_more"
    return "kill"


def ad_stats(project_name):
    """Latest (clicks, spend) recorded by the ad cap check, or (None, None)."""
    from .google_ads import _load_state
    for c in _load_state():
        if c["project"] == project_name and "clicks" in c:
            return c["clicks"], c.get("spent_usd", 0)
    return None, None


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
    clicks, spend = ad_stats(project_name)
    if clicks is not None:
        print(f"  Ad clicks: {clicks}  |  Spend: ${spend:.2f}")

    verdict = decide(total, strong, clicks, spend)
    if verdict == "build":
        status = "building"
        emoji = "🚀"
        reason = f"{strong} people signalled strong spend intent — enough to build."
        next_steps = "• Set up payment page\n• Schedule founder calls\n• Run outreach drafts"
    elif verdict == "extend":
        status = "validating"
        emoji = "⏳"
        reason = f"Only {clicks} ad clicks (need {MIN_CLICKS}) — too few to judge {total} signups."
        next_steps = "• Extend the ad budget until ~100 clicks\n• Check keywords have search volume"
    elif verdict == "validate_more":
        status = "validating"
        emoji = "🔁"
        reason = f"{total} signups but only {strong} strong spend signals — extend or pivot messaging."
        next_steps = "• Try a different headline\n• Run outreach to convert soft signals\n• Consider a price drop"
    else:
        status = "killed"
        emoji = "🔴"
        reason = (f"{total} signups from {clicks} clicks (${spend:.2f}) — over ${MAX_COST_PER_SIGNUP}/signup."
                  if clicks is not None else f"Only {total} signups after 7 days — not enough signal.")
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


if __name__ == "__main__":
    assert decide(0, 3, 10, 30) == "build"
    assert decide(0, 0, 15, 45) == "extend"           # day-3 zero is not a kill
    assert decide(2, 0, 100, 100) == "validate_more"  # $50/signup
    assert decide(1, 0, 120, 100) == "kill"           # $100/signup
    assert decide(0, 0, 120, 100) == "kill"
    assert decide(5, 0) == "validate_more" and decide(4, 0) == "kill"  # no ad data
    print("ok")
