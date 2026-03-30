"""
Daily monitor for active validation campaigns.
Reads Tally form responses, computes metrics, posts summary to Slack.
"""

import json
import os
import urllib.parse
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


def register_campaign(project_name, form_id, pages_url, notion_page_id=None, pain_desire=None, price_per_year=None, days=7):
    """Called after a successful deploy to track the campaign."""
    campaigns = load_campaigns()
    # Replace existing entry for same project
    campaigns = [c for c in campaigns if c["project"] != project_name]
    campaigns.append({
        "project": project_name,
        "form_id": form_id,
        "pages_url": pages_url,
        "notion_page_id": notion_page_id,
        "pain_desire": pain_desire,
        "price_per_year": price_per_year,
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


SHEETS_ID = "1UO2fp_kUUj2Go8VZ6nJtdoYhzJDAvrUIVM0Wvp5fg_Y"
SA_KEY_FILE = "/home/ubuntu/google-service-account.json"


def _sheets_token():
    """Get a Google API access token using the service account."""
    import time, base64, hashlib, hmac
    with open(SA_KEY_FILE) as f:
        sa = json.load(f)
    now = int(time.time())
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=")
    payload = base64.urlsafe_b64encode(json.dumps({
        "iss": sa["client_email"],
        "scope": "https://www.googleapis.com/auth/spreadsheets.readonly",
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now, "exp": now + 3600,
    }).encode()).rstrip(b"=")
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.backends import default_backend
    key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None, backend=default_backend())
    sig = base64.urlsafe_b64encode(key.sign(header + b"." + payload, padding.PKCS1v15(), hashes.SHA256())).rstrip(b"=")
    jwt = (header + b"." + payload + b"." + sig).decode()
    body = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt,
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body,
                                  headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())["access_token"]


def get_formspree_responses(project_name):
    """Fetch signups for a project from Google Sheets."""
    import urllib.parse
    if not os.path.exists(SA_KEY_FILE):
        print("  No service account key — skipping response fetch")
        return []
    try:
        token = _sheets_token()
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEETS_ID}/values/A:F"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        rows = data.get("values", [])
        if not rows:
            return []
        headers = [h.strip().lower() for h in rows[0]]
        results = []
        for row in rows[1:]:
            d = dict(zip(headers, row + [""] * len(headers)))
            if d.get("project", "").strip().lower() == project_name.strip().lower():
                results.append({"data": d})
        return results
    except Exception as e:
        print(f"  Sheets read failed: {e}")
        return []


def run_monitor(dry_run=False):

    campaigns = load_campaigns()
    active = [c for c in campaigns if c.get("status") == "active"]

    if not active:
        print("No active campaigns to monitor.")
        return

    for campaign in active:
        project = campaign["project"]
        pages_url = campaign["pages_url"]
        total_days = campaign.get("days", 7)
        day = days_elapsed(campaign["start_date"]) + 1

        print(f"\nChecking campaign: {project} (day {day}/{total_days})")

        try:
            responses = get_formspree_responses(project)
        except Exception as e:
            print(f"  Failed to fetch responses: {e}")
            responses = []

        total = len(responses)
        spend_counts = {}
        for r in responses:
            v = r.get("data", {}).get("how much would you pay for this service?", "")
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

        # Day 5: auto-generate outreach drafts
        if day == 5 and not campaign.get("outreach_sent"):
            print(f"  Day 5 — generating outreach drafts...")
            try:
                from phase2.outreach import run_outreach
                run_outreach(
                    project, campaign.get("pain_desire", ""),
                    campaign.get("price_per_year"), dry_run=dry_run,
                )
                campaign["outreach_sent"] = True
            except Exception as e:
                print(f"  Outreach failed: {e}")

        # Day 7: auto-run kill/build decision
        if day >= total_days and not campaign.get("decision_sent"):
            print(f"  Day 7 — running kill/build decision...")
            try:
                from phase2.decision import run_decision
                run_decision(
                    project, campaign.get("notion_page_id"),
                    campaign.get("pain_desire", ""), campaign.get("price_per_year"),
                    dry_run=dry_run,
                )
                campaign["decision_sent"] = True
                campaign["status"] = "ended"
            except Exception as e:
                print(f"  Decision failed: {e}")

        # Mark campaign as ended if past duration
        if day > total_days:
            campaign["status"] = "ended"

    save_campaigns(campaigns)
