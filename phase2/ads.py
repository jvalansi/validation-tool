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
import urllib.parse
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


def generate_business_description(project_name, description, pain_desire):
    prompt = f"""Write a Google Ads business description for the "Describe what makes your business unique" field.

Project: {project_name}
Description: {description}
Pain it solves: {pain_desire}

Rules:
- 2-3 sentences max, under 200 words
- Lead with what makes it unique / the core mechanism
- Mention the pain it solves and who it's for
- Plain English, no jargon, no exclamation marks

Return only the description text, nothing else."""

    claude_path = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    result = subprocess.run(
        [claude_path, "-p", prompt, "--output-format", "json", "--dangerously-skip-permissions"],
        capture_output=True, text=True, timeout=120,
        env=env, cwd="/home/ubuntu",
    )
    if result.returncode != 0:
        return description
    outer = json.loads(result.stdout)
    return outer.get("result", "").strip().strip('"')


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


SA_KEY_FILE = "/home/ubuntu/google-service-account.json"
ADS_SHEET_ID = "1J7xl36Jl9vAK5ax2WHItcqlaniw-9c1kmb18wafdDB0"


def _sheets_token():
    import time, base64
    with open(SA_KEY_FILE) as f:
        sa = json.load(f)
    now = int(time.time())
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=")
    payload = base64.urlsafe_b64encode(json.dumps({
        "iss": sa["client_email"],
        "scope": "https://www.googleapis.com/auth/spreadsheets",
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
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())["access_token"]


def write_csv_to_sheet(csv_content: str, tab_name: str, sheet_id: str = ADS_SHEET_ID) -> str:
    """Write CSV data to a new tab in an existing Google Sheet. Returns the sheet URL."""
    import csv, io

    token = _sheets_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def sheets_request(method, path, data=None):
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(
            f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}{path}",
            data=body, headers=headers, method=method,
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())

    # Find or create the sheet tab
    meta = sheets_request("GET", "")
    existing = [(s["properties"]["title"], s["properties"]["sheetId"]) for s in meta["sheets"]
                if s["properties"]["title"] == tab_name]
    if existing:
        new_sheet_id = existing[0][1]
        # Clear existing content
        body = json.dumps({}).encode()
        req = urllib.request.Request(
            f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/"
            f"{urllib.parse.quote(tab_name)}:clear",
            data=body, headers=headers, method="POST",
        )
        with urllib.request.urlopen(req, timeout=15):
            pass
    else:
        result = sheets_request("POST", ":batchUpdate", {"requests": [{"addSheet": {"properties": {"title": tab_name}}}]})
        new_sheet_id = result["replies"][0]["addSheet"]["properties"]["sheetId"]

    # Parse CSV into rows
    rows = list(csv.reader(io.StringIO(csv_content)))

    # Write data
    body = json.dumps({"values": rows, "majorDimension": "ROWS"}).encode()
    req = urllib.request.Request(
        f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/"
        f"{urllib.parse.quote(tab_name)}!A1?valueInputOption=RAW",
        data=body, headers=headers, method="PUT",
    )
    with urllib.request.urlopen(req, timeout=15):
        pass

    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={new_sheet_id}"


def build_editor_csv(config: dict) -> str:
    """Build a Google Ads Editor bulk-import CSV from an ads config dict."""
    import csv, io

    campaign = config["campaign"]
    ad_group = config["ad_group"]
    rsa = config["rsa"]
    keywords = ad_group["keywords"]

    headers = [
        "Campaign", "Campaign type", "Campaign status",
        "Budget", "Budget type", "Bid strategy type",
        "Languages", "Location", "Location type",
        "Ad group", "Ad group status",
        "Keyword", "Match type", "Keyword status",
        "Ad type", "Ad status",
        *[f"Headline {i}" for i in range(1, 16)],
        *[f"Description {i}" for i in range(1, 5)],
        "Final URL",
    ]

    def row(**kwargs):
        return {h: kwargs.get(h, "") for h in headers}

    rows = []

    # Campaign row
    rows.append(row(**{
        "Campaign": campaign["name"],
        "Campaign type": "Search",
        "Campaign status": "Enabled",
        "Budget": str(campaign["daily_budget_usd"]),
        "Budget type": "Daily",
        "Bid strategy type": "Maximize clicks",
        "Languages": "English",
    }))

    # Location targeting rows
    for location in ["United States", "United Kingdom", "Canada", "Australia"]:
        rows.append(row(**{
            "Campaign": campaign["name"],
            "Location": location,
            "Location type": "Include",
        }))

    # Ad group row
    rows.append(row(**{
        "Campaign": campaign["name"],
        "Ad group": ad_group["name"],
        "Ad group status": "Enabled",
    }))

    # Keyword rows — strip quote/bracket syntax, set Match type column
    for kw in keywords.get("broad", []):
        rows.append(row(**{"Campaign": campaign["name"], "Ad group": ad_group["name"],
                           "Keyword": kw, "Match type": "Broad", "Keyword status": "Enabled"}))
    for kw in keywords.get("phrase", []):
        rows.append(row(**{"Campaign": campaign["name"], "Ad group": ad_group["name"],
                           "Keyword": kw.strip('"'), "Match type": "Phrase", "Keyword status": "Enabled"}))
    for kw in keywords.get("exact", []):
        rows.append(row(**{"Campaign": campaign["name"], "Ad group": ad_group["name"],
                           "Keyword": kw.strip("[]"), "Match type": "Exact", "Keyword status": "Enabled"}))

    # RSA row
    headlines = rsa.get("headlines", [])
    descriptions = rsa.get("descriptions", [])
    ad_row = row(**{
        "Campaign": campaign["name"],
        "Ad group": ad_group["name"],
        "Ad type": "Responsive search ad",
        "Ad status": "Enabled",
        "Final URL": rsa.get("final_url", ""),
        **{f"Headline {i+1}": h for i, h in enumerate(headlines)},
        **{f"Description {i+1}": d for i, d in enumerate(descriptions)},
    })
    rows.append(ad_row)

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


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
    print(f"\n[Ads] Generating business description for {project_name}...")
    business_desc = generate_business_description(project_name, description, pain_desire)

    print(f"[Ads] Generating keywords...")
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
        "business_description": business_desc,
    }

    # Save JSON locally
    os.makedirs(DATA_DIR, exist_ok=True)
    out_path = os.path.join(DATA_DIR, f"ads_{_slug(project_name)}.json")
    with open(out_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"[Ads] Saved to {out_path}")

    # Generate CSV and write to Google Sheet tab
    csv_content = build_editor_csv(config)
    sheet_url = None
    tab_name = f"ads_{_slug(project_name)}"
    if not dry_run:
        try:
            sheet_url = write_csv_to_sheet(csv_content, tab_name)
            print(f"[Ads] CSV written to sheet tab '{tab_name}': {sheet_url}")
        except Exception as e:
            print(f"[Ads] Sheet write failed: {e}")
    else:
        csv_path = os.path.join(DATA_DIR, f"ads_{_slug(project_name)}.csv")
        with open(csv_path, "w") as f:
            f.write(csv_content)
        print(f"[Ads] CSV saved locally (dry-run): {csv_path}")

    # Build Slack message
    kw = keywords
    kw_lines = (
        "\n".join(f"  {k}" for k in kw.get("broad", []))
        + "\n".join(f"  {k}" for k in kw.get("phrase", []))
        + "\n".join(f"  {k}" for k in kw.get("exact", []))
    )
    headlines_str = "\n".join(f"  {i+1}. {h}" for i, h in enumerate(ad_copy.get("headlines", [])))
    descs_str = "\n".join(f"  {i+1}. {d}" for i, d in enumerate(ad_copy.get("descriptions", [])))

    ads_ui_url = "https://ads.google.com/aw/campaigns/new/express?campaignType=SEARCH"
    msg_header = (
        f"*{project_name} — Google Ads Config*\n"
        f"Budget: ${daily_budget}/day  |  Landing page: {landing_url or '(none yet)'}\n"
        f"<{ads_ui_url}|Create campaign in Google Ads UI> — paste the keywords and copy below"
    )

    msg_business = f"*Business description* (paste into \"Describe what makes your business unique\")\n```{business_desc}```"
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
        + (f"\n<{sheet_url}|Open Google Ads Editor CSV in Sheets> — File → Download → CSV" if sheet_url else "")
    )

    if dry_run:
        print(msg_header)
        print(f"Create campaign: {ads_ui_url}")
        print(msg_business)
        print(msg_keywords)
        print(msg_copy)
        print(msg_settings)
    else:
        ts = _slack(msg_header)
        _slack(msg_business, thread_ts=ts)
        _slack(msg_keywords, thread_ts=ts)
        _slack(msg_copy, thread_ts=ts)
        _slack(msg_settings, thread_ts=ts)

    return {"status": "generated", "config_path": out_path, "config": config}
