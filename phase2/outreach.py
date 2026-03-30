"""
Generate personalised outreach drafts for waitlist signups using Claude.
Posts drafts to Slack for manual review and sending.
"""

import json
import os
import subprocess
import urllib.request

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "#proj-project-validation"


def _slack(text, thread_ts=None):
    if not SLACK_BOT_TOKEN:
        print(f"[Slack] {text}")
        return None
    payload = {"channel": SLACK_CHANNEL, "text": text}
    if thread_ts:
        payload["thread_ts"] = thread_ts
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=body,
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
        return result.get("ts")


def _claude(prompt):
    result = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "text"],
        capture_output=True, text=True, timeout=60,
        env=os.environ.copy(),
    )
    return result.stdout.strip()


def generate_draft(project_name, pain_desire, price_per_year, email, spend, role):
    def _saas_price(annual):
        raw = annual / 12
        anchors = [9, 19, 29, 49, 79, 99, 149, 199, 299, 499, 799, 999]
        return min(anchors, key=lambda x: abs(x - raw))

    price_mo = _saas_price(price_per_year) if price_per_year else None
    price_str = f"${price_mo}/mo" if price_mo else "a founding price"

    role_str = f" They said their role is: {role}." if role else ""
    spend_str = f" They indicated they'd pay: {spend}." if spend else ""

    prompt = f"""Write a short, personal cold outreach email to someone who signed up for early access to {project_name}.

Product context: {pain_desire}
Founder pricing: {price_str}

About this person:{spend_str}{role_str}

Guidelines:
- 4-6 sentences max
- Casual and genuine, not salesy
- Acknowledge their specific spend/role if available
- End with a soft ask: 15-min call OR locking in founder pricing at {price_str}
- No subject line, just the email body
- Sign off as "The {project_name} team"

Write only the email body, nothing else."""

    return _claude(prompt)


def run_outreach(project_name, pain_desire, price_per_year, dry_run=False):
    from phase2.monitor import get_formspree_responses, load_campaigns

    # Find the campaign
    campaigns = load_campaigns()
    campaign = next((c for c in campaigns if c["project"] == project_name), None)
    if not campaign:
        print(f"No campaign found for {project_name}")
        return

    responses = get_formspree_responses(project_name)
    if not responses:
        print(f"No signups yet for {project_name}")
        return

    print(f"Generating outreach drafts for {len(responses)} signups...")

    header_ts = None
    if not dry_run:
        header_ts = _slack(f"*{project_name} — Outreach Drafts ({len(responses)} signups)*\nReview each draft below and send manually.")

    for i, r in enumerate(responses, 1):
        d = r.get("data", {})
        email = d.get("email", "unknown")
        spend = d.get("how much would you pay for this service?", "")
        role  = d.get("your role (optional)", "")

        print(f"  [{i}] {email} ({role or 'no role'}, {spend or 'no spend'})")

        draft = generate_draft(project_name, pain_desire, price_per_year, email, spend, role)

        msg = f"*To:* {email}"
        if role:  msg += f"  |  *Role:* {role}"
        if spend: msg += f"  |  *Spend intent:* {spend}"
        msg += f"\n\n{draft}"

        if dry_run:
            print(msg)
            print()
        else:
            _slack(msg, thread_ts=header_ts)

    print("Done.")
