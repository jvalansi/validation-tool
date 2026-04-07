#!/usr/bin/env python3
"""
Create and validate a new Notion project page from a raw idea.

Runs the full pipeline:
  1. Claude generates search queries, description, work plan
  2. validation_tool.py report fetches market signals
  3. Numbers are OOM-rounded (prices to nearest power of 10, WW to nearest 5)
  4. Probability mapped to user scale: 0.01 moonshot / 0.10 standard / 1.0 straightforward
  5. Notion page created with all properties + body content

Usage:
  python notion_create.py "Promptware" "A system to reduce LLM inference costs via smart prompting"
  python notion_create.py --name NAME --idea DESCRIPTION [--dry-run]
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"
NOTION_DB = "17731083-1fdd-4c06-a3c3-c87aa758703a"
VALIDATION_TOOL = os.path.join(os.path.dirname(__file__), "validation_tool.py")
PYTHON = "/home/ubuntu/miniconda3/bin/python"
STATUS_TODO = "\u23f3"


# ---------------------------------------------------------------------------
# Notion helpers
# ---------------------------------------------------------------------------

def _notion_request(path, data=None, method=None):
    body = json.dumps(data).encode() if data else None
    if method is None:
        method = "PATCH" if body else "GET"
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        data=body,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            **({"Content-Type": "application/json"} if body else {}),
        },
        method=method,
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def notion_post(path, data):
    return _notion_request(path, data, method="POST")


def notion_patch(path, data):
    return _notion_request(path, data, method="PATCH")


# ---------------------------------------------------------------------------
# Rounding helpers
# ---------------------------------------------------------------------------

def round_ww(ww):
    """Round work weeks to nearest 5 (min 5)."""
    return max(5, round(ww / 5) * 5)


# ---------------------------------------------------------------------------
# Step 1: Claude enrichment
# ---------------------------------------------------------------------------

ENRICHMENT_PROMPT = """\
You are a startup validation assistant. Given a project idea, generate structured data
for a validation pipeline. Return ONLY valid JSON with no markdown.

Project Name: {name}
Idea: {idea}

Return this exact JSON structure:
{{
  "description": "2-3 sentence product description: what it does and who it's for",
  "validation_query": "4-8 word search query targeting the PAIN/PROBLEM (not the solution name), optimized for HN/Reddit discussion discovery",
  "trends_query": "2-4 word Google Trends query for the underlying market topic",
  "pain_desire": "1-2 sentences on the specific pain companies/users feel that this solves",
  "target_customer": "1 sentence describing the ideal customer",
  "what_it_is": "2-3 sentences describing the product from a customer perspective (benefits-first)",
  "work_weeks": <integer rounded to nearest 5, solo dev MVP estimate>,
  "work_plan": [
    "Wk 1-N: <concrete milestone>",
    "Wk N-N: <concrete milestone>"
  ]
}}

Rules:
- validation_query: focus on the pain (e.g. "LLM API bills too expensive" not "LLM cost optimizer")
- trends_query: short, high-volume topic keywords (e.g. "LLM cost" not "LLM cost optimization tool")
- work_weeks: nearest 5 (5, 10, 15, 20, 25...) for a focused solo MVP
- work_plan: 3-5 items covering core MVP milestones\
"""


def claude_enrichment(name, idea):
    claude_path = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    prompt = ENRICHMENT_PROMPT.format(name=name, idea=idea)
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    result = subprocess.run(
        [claude_path, "-p", prompt, "--output-format", "json", "--dangerously-skip-permissions"],
        capture_output=True, text=True, timeout=60,
        env=env, cwd="/home/ubuntu",
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claude enrichment failed: {result.stderr[:200]}")
    outer = json.loads(result.stdout)
    text = outer.get("result", "").strip()
    if text.startswith("```"):
        text = "\n".join(text.split("\n")[1:]).rsplit("```", 1)[0].strip()
    start, end = text.find("{"), text.rfind("}") + 1
    return json.loads(text[start:end])


# ---------------------------------------------------------------------------
# Step 2: Run validation tool
# ---------------------------------------------------------------------------

def run_validation(validation_query, trends_query=None):
    cmd = [PYTHON, VALIDATION_TOOL, "report", "--query", validation_query, "--assume-tech-exists"]
    if trends_query:
        cmd += ["--trends-query", trends_query]
    print(f"  cmd: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    if result.returncode != 0:
        print(f"  Warning: validation error — {result.stderr[:200]}", file=sys.stderr)
        return None
    return json.loads(result.stdout)


# ---------------------------------------------------------------------------
# Step 3: Build page body blocks
# ---------------------------------------------------------------------------

def build_blocks(enriched, report):
    claude = report.get("claude_analysis", {}) if report else {}
    sources = report.get("sources", {}) if report else {}
    blocks = []

    def h2(text):
        return {"heading_2": {"rich_text": [{"text": {"content": text}}]}}

    def para(text):
        return {"paragraph": {"rich_text": [{"text": {"content": text}}]}}

    def bullet(text):
        return {"bulleted_list_item": {"rich_text": [{"text": {"content": text}}]}}

    blocks += [h2("What It Is"), para(enriched["what_it_is"])]
    blocks += [h2("Target Customer"), para(enriched["target_customer"])]

    # Validation signals
    signal_lines = []
    gt = sources.get("google_trends", {})
    if "average_interest" in gt:
        signal_lines.append(
            f"Google Trends: {gt['average_interest']}/100 avg, {gt.get('trend_direction', '?')}"
        )
    hn = sources.get("hacker_news", {})
    if hn.get("total_results", 0):
        top = hn.get("top_posts", [{}])[0]
        signal_lines.append(
            f"HN: {hn['total_results']} results — top: \"{top.get('title', '')}\" ({top.get('points', 0)} pts)"
        )
    rd = sources.get("reddit", {})
    if rd.get("total_results", 0):
        signal_lines.append(f"Reddit: {rd['total_results']} results")
    ph = sources.get("product_hunt", {})
    if ph.get("existing_products", 0):
        top_ph = ph.get("top_products", [{}])[0]
        signal_lines.append(
            f"Product Hunt: {ph['existing_products']} products — top: \"{top_ph.get('name', '')}\""
        )
    if signal_lines:
        blocks.append(h2("Validation Signals"))
        blocks += [bullet(s) for s in signal_lines]

    # Risks & Opportunities
    risks = claude.get("key_risks", [])
    opps = claude.get("key_opportunities", [])
    if risks:
        blocks.append(h2("Key Risks"))
        blocks += [bullet(r) for r in risks]
    if opps:
        blocks.append(h2("Opportunities"))
        blocks += [bullet(o) for o in opps]

    # Work plan
    blocks.append(h2("Work Plan"))
    blocks += [bullet(step) for step in enriched.get("work_plan", [])]

    return blocks


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Create and validate a Notion project from a raw idea"
    )
    parser.add_argument("name", nargs="?", help="Project name")
    parser.add_argument("idea", nargs="?", help="Idea description")
    parser.add_argument("--name", dest="name_flag", help="Project name (flag form)")
    parser.add_argument("--idea", dest="idea_flag", help="Idea description (flag form)")
    parser.add_argument("--dry-run", action="store_true", help="Print output without writing to Notion")
    args = parser.parse_args()

    name = args.name_flag or args.name
    idea = args.idea_flag or args.idea
    if not name or not idea:
        parser.print_help()
        sys.exit(1)

    if not NOTION_TOKEN and not args.dry_run:
        print("Error: NOTION_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    # 1. Claude enrichment
    print("Step 1/3: Enriching idea with Claude...")
    enriched = claude_enrichment(name, idea)
    print(f"  validation_query: {enriched['validation_query']}")
    print(f"  trends_query:     {enriched['trends_query']}")
    print(f"  work_weeks:       {enriched['work_weeks']}")

    # 2. Run validation
    print("\nStep 2/3: Running validation tool...")
    report = run_validation(enriched["validation_query"], enriched.get("trends_query"))

    # 3. Extract & round numbers
    claude_analysis = (report or {}).get("claude_analysis", {})
    sources = (report or {}).get("sources", {})
    signal_count = (report or {}).get("summary", {}).get("signal_count", 0)
    tam_tier = (report or {}).get("revenue_estimate", {}).get("tam_tier", "niche")

    price_rounded = claude_analysis.get("price_per_customer_annual") or 100
    tam_rounded = claude_analysis.get("tam_customers") or 10000
    probability = claude_analysis.get("suggested_probability") or 0.01
    ww_rounded = round_ww(enriched["work_weeks"])

    trends_avg = sources.get("google_trends", {}).get("average_interest")
    hn_results = sources.get("hacker_news", {}).get("total_results")
    reddit_results = sources.get("reddit", {}).get("total_results")
    ph_products = sources.get("product_hunt", {}).get("existing_products")

    if signal_count >= 3:
        market_signal = "High"
    elif signal_count >= 1:
        market_signal = "Low"
    else:
        market_signal = "Low"

    print(f"\n  price/yr:      ${price_rounded}")
    print(f"  TAM customers: {tam_rounded:,}")
    print(f"  work weeks:    {ww_rounded}")
    print(f"  probability:   {probability} ({probability*100:.0f}%)")
    print(f"  market signal: {market_signal}")

    if args.dry_run:
        print("\n[dry-run] Skipping Notion write. Enriched data:")
        print(json.dumps(enriched, indent=2))
        return

    # 4. Create Notion page
    print("\nStep 3/3: Creating Notion page...")
    props = {
        "Project": {"title": [{"text": {"content": name}}]},
        "Description": {"rich_text": [{"text": {"content": enriched["description"]}}]},
        "Validation Query": {"rich_text": [{"text": {"content": enriched["validation_query"]}}]},
        "Trends Query": {"rich_text": [{"text": {"content": enriched["trends_query"]}}]},
        "Pain/Desire": {"rich_text": [{"text": {"content": enriched["pain_desire"]}}]},
        "Work Weeks": {"number": ww_rounded},
        "Price/Customer/yr ($)": {"number": price_rounded},
        "TAM Customers": {"number": tam_rounded},
        "Probability": {"number": probability},
        "Market Signal": {"select": {"name": market_signal}},
        "TAM Tier": {"select": {"name": tam_tier}},
        "\u05e1\u05d8\u05d8\u05d5\u05e1": {"status": {"name": STATUS_TODO}},
    }
    if trends_avg is not None:
        props["Trends Interest"] = {"number": float(trends_avg)}
    if hn_results is not None:
        props["HN Results"] = {"number": int(hn_results)}
    if reddit_results is not None:
        props["Reddit Results"] = {"number": int(reddit_results)}
    if ph_products is not None:
        props["PH Products"] = {"number": int(ph_products)}

    page = notion_post("pages", {"parent": {"database_id": NOTION_DB}, "properties": props})
    page_id = page["id"]
    page_url = page.get("url", "")
    print(f"  Created: {page_url}")

    # 5. Add page body
    blocks = build_blocks(enriched, report)
    for i in range(0, len(blocks), 100):
        notion_patch(f"blocks/{page_id}/children", {"children": blocks[i:i + 100]})

    print(f"\nDone! {page_url}")


if __name__ == "__main__":
    main()
