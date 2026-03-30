"""
Generate Google Ads campaign config using Claude.

Outputs:
- Keywords (broad/phrase/exact) for manual entry
- RSA headlines (15 × ≤30 chars) and descriptions (4 × ≤90 chars)
- Suggested campaign settings

Posts config to Slack and saves to data/ads_<slug>.json.
"""

import json
import os
import re
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "#proj-project-validation"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


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
        return json.loads(r.read()).get("ts")


def _claude_json(prompt):
    claude_path = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    result = subprocess.run(
        [claude_path, "-p", prompt, "--output-format", "json", "--dangerously-skip-permissions"],
        capture_output=True, text=True, timeout=120,
        env=env, cwd="/home/ubuntu",
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claude failed: {result.stderr}")
    outer = json.loads(result.stdout)
    text = outer.get("result", "").strip()
    if text.startswith("```"):
        text = "\n".join(text.split("\n")[1:]).rsplit("```", 1)[0].strip()
    return json.loads(text)


def generate_keywords(project_name, validation_query, pain_desire):
    prompt = f"""Generate a Google Ads keyword list for a Search campaign.

Project: {project_name}
Validation Query: {validation_query}
Pain/Desire: {pain_desire}

Rules:
- 15 keywords total: 5 broad match, 5 phrase match, 5 exact match
- Focus on problem-framing terms (what the user types when they have the pain), not product names
- Phrase match: wrap in double quotes, e.g. "reduce llm costs"
- Exact match: wrap in square brackets, e.g. [llm cost optimization]
- Broad match: plain text, e.g. reduce openai api costs
- Avoid branded terms and overly generic single words

Return a JSON object with keys "broad", "phrase", "exact" — each an array of 5 strings (include the quote/bracket syntax in phrase/exact values).
Return only valid JSON, no markdown."""

    return _claude_json(prompt)


def generate_ad_copy(project_name, description, pain_desire, landing_url):
    prompt = f"""Generate a Google Responsive Search Ad (RSA) for a Search campaign.

Project: {project_name}
Description: {description}
Pain/Desire: {pain_desire}
Landing page: {landing_url}

Rules:
- 15 headlines, each ≤30 characters (including spaces). Count carefully.
- 4 descriptions, each ≤90 characters (including spaces). Count carefully.
- Mix angles: pain statement, solution, social proof hook, CTA, urgency
- No exclamation marks in headlines (Google policy)
- No repetition across headlines
- CTAs like: "Join the Beta", "Get Early Access", "See How It Works", "Try Free"

Return a JSON object with keys "headlines" (array of 15 strings) and "descriptions" (array of 4 strings).
Return only valid JSON, no markdown."""

    return _claude_json(prompt)


def _saas_price(annual):
    if not annual:
        return None
    raw = annual / 12
    anchors = [9, 19, 29, 49, 79, 99, 149, 199, 299, 499]
    return min(anchors, key=lambda x: abs(x - raw))


def generate_ads_config(
    project_name,
    description,
    pain_desire,
    validation_query,
    price_per_year,
    landing_url,
    daily_budget=15,
    dry_run=False,
):
    print(f"\n[Ads] Generating keywords for {project_name}...")
    keywords = generate_keywords(project_name, validation_query or pain_desire, pain_desire)

    print(f"[Ads] Generating RSA ad copy...")
    ad_copy = generate_ad_copy(project_name, description, pain_desire, landing_url or "")

    price_mo = _saas_price(price_per_year)

    config = {
        "project": project_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "campaign": {
            "name": f"Validate - {project_name}",
            "type": "Search",
            "daily_budget_usd": daily_budget,
            "geo": "United States, United Kingdom, Canada, Australia",
            "language": "English",
            "bidding": "Maximize Clicks",
            "start_immediately": True,
        },
        "ad_group": {
            "name": project_name,
            "keywords": keywords,
        },
        "rsa": {
            "headlines": ad_copy.get("headlines", []),
            "descriptions": ad_copy.get("descriptions", []),
            "final_url": landing_url or "",
        },
        "suggested_price_anchor": f"${price_mo}/mo" if price_mo else None,
    }

    # Save to data/
    os.makedirs(DATA_DIR, exist_ok=True)
    out_path = os.path.join(DATA_DIR, f"ads_{_slug(project_name)}.json")
    with open(out_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"[Ads] Saved to {out_path}")

    # Build Slack message
    kw = keywords
    kw_lines = (
        "\n".join(f"  {k}" for k in kw.get("broad", []))
        + "\n".join(f"  {k}" for k in kw.get("phrase", []))
        + "\n".join(f"  {k}" for k in kw.get("exact", []))
    )
    headlines_str = "\n".join(f"  {i+1}. {h}" for i, h in enumerate(ad_copy.get("headlines", [])))
    descs_str = "\n".join(f"  {i+1}. {d}" for i, d in enumerate(ad_copy.get("descriptions", [])))

    msg_header = (
        f"*{project_name} — Google Ads Config*\n"
        f"Budget: ${daily_budget}/day  |  Landing page: {landing_url or '(none yet)'}\n"
        f"_Paste into Google Ads UI: New Campaign → Search → manually enter below_"
    )

    msg_keywords = f"*Keywords*\n```{kw_lines}```"
    msg_copy = f"*RSA Headlines* (15 — paste all, Google picks best combos)\n```{headlines_str}```\n\n*Descriptions*\n```{descs_str}```"
    msg_settings = (
        f"*Campaign settings*\n"
        f"• Type: Search\n"
        f"• Budget: ${daily_budget}/day\n"
        f"• Bidding: Maximize Clicks\n"
        f"• Geo: {config['campaign']['geo']}\n"
        f"• Language: English\n"
        + (f"• Price anchor on landing page: {config['suggested_price_anchor']}\n" if config['suggested_price_anchor'] else "")
        + f"\nFull config saved to `{out_path}`"
    )

    if dry_run:
        print(msg_header)
        print(msg_keywords)
        print(msg_copy)
        print(msg_settings)
    else:
        ts = _slack(msg_header)
        _slack(msg_keywords, thread_ts=ts)
        _slack(msg_copy, thread_ts=ts)
        _slack(msg_settings, thread_ts=ts)

    return {"status": "generated", "config_path": out_path, "config": config}
