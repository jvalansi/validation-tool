#!/usr/bin/env python3
"""
Run validation report for a Notion project and write results back.

Usage:
  python notion_validate.py <page-id>
  python notion_validate.py <page-id> --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request


NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"
VALIDATION_TOOL = os.path.join(os.path.dirname(__file__), "validation_tool.py")
PYTHON = "/home/ubuntu/miniconda3/bin/python"


def notion_get(path):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        headers={"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": NOTION_VERSION},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def notion_patch(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        data=body,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        method="PATCH",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def get_text(prop):
    items = prop.get("rich_text") or prop.get("title") or []
    return items[0].get("plain_text", "") if items else ""


def notion_delete(path):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        headers={"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": NOTION_VERSION},
        method="DELETE",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        resp.read()


def get_page_blocks(page_id):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers={"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": NOTION_VERSION},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read()).get("results", [])


def remove_existing_validation_section(blocks):
    found = False
    for b in blocks:
        if not found:
            t = b["type"]
            text = "".join(x.get("plain_text", "") for x in b.get(t, {}).get("rich_text", []))
            if t == "heading_2" and "Validation" in text:
                found = True
        if found:
            try:
                notion_delete(f"blocks/{b['id']}")
            except Exception:
                pass


def append_validation_section(page_id, report, new_prob, claude):
    gt = report["sources"].get("google_trends", {})
    hn = report["sources"].get("hacker_news", {})
    rd = report["sources"].get("reddit", {})
    ph = report["sources"].get("product_hunt", {})

    gt_line = (
        f"📈 Google Trends: {gt['average_interest']}/100 avg, trend {gt.get('trend_direction', 'unknown')}"
        if "average_interest" in gt else "📈 Google Trends: no data"
    )
    hn_line = f"🟡 Hacker News: {hn.get('total_results', 0)} results"
    if hn.get("top_posts"):
        top = hn["top_posts"][0]
        hn_line += f" — top: \"{top['title']}\" ({top['points']} pts)"
    rd_line = f"💬 Reddit: {rd.get('total_results', 0)} results"
    if rd.get("top_posts"):
        rd_line += f" — top: \"{rd['top_posts'][0]['title']}\""
    ph_existing = ph.get("existing_products", -1)
    if ph_existing == -1:
        ph_line = "🔍 Product Hunt: skipped"
    elif ph_existing == 0:
        ph_line = "🔍 Product Hunt: no matching products found"
    else:
        ph_line = f"🔍 Product Hunt: {ph_existing} matching product(s)"
        if ph.get("top_products"):
            ph_line += f" — top: \"{ph['top_products'][0]['name']}\""

    verdict = report.get("summary", {}).get("verdict", "")
    signals = report.get("summary", {}).get("positive_signals", [])

    blocks = [
        {"heading_2": {"rich_text": [{"text": {"content": "Validation (Mar 2026)"}}]}},
        {"heading_3": {"rich_text": [{"text": {"content": "Signals"}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": gt_line}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": hn_line}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": rd_line}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": ph_line}}]}},
    ]
    if signals:
        blocks.append({"bulleted_list_item": {"rich_text": [{"text": {"content": "✅ " + ", ".join(signals)}}]}})

    blocks += [
        {"heading_3": {"rich_text": [{"text": {"content": "Verdict"}}]}},
        {"callout": {
            "rich_text": [{"text": {"content": f"{verdict}. Probability: {new_prob*100:.0f}%."}}],
            "icon": {"type": "emoji", "emoji": "🧪"}
        }},
    ]

    if claude:
        prob_reasoning = claude.get("probability_reasoning", "")
        value_reasoning = claude.get("value_reasoning", "")
        tam = claude.get("tam_assessment", "")
        pricing = claude.get("pricing_assessment", "")
        if prob_reasoning:
            blocks.append({"quote": {"rich_text": [{"text": {"content": f"🎲 {prob_reasoning}"}}]}})
        if value_reasoning:
            blocks.append({"quote": {"rich_text": [{"text": {"content": f"💰 {value_reasoning}"}}]}})
        if tam:
            blocks.append({"heading_3": {"rich_text": [{"text": {"content": "Market Analysis"}}]}})
            blocks.append({"paragraph": {"rich_text": [{"text": {"content": tam}}]}})
        if pricing:
            blocks.append({"bulleted_list_item": {"rich_text": [{"text": {"content": f"💰 Pricing: {pricing}"}}]}})

    req = urllib.request.Request(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        data=json.dumps({"children": blocks}).encode(),
        method="PATCH",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


def run_validation(query, pain_query=None):
    cmd = [PYTHON, VALIDATION_TOOL, "report", "--query", query]
    if pain_query:
        cmd += ["--pain-query", pain_query, "--assume-tech-exists"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        print(f"Validation error: {result.stderr[:200]}", file=sys.stderr)
        return None
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description="Validate a Notion project and write results back")
    parser.add_argument("page_id", help="Notion page ID")
    parser.add_argument("--dry-run", action="store_true", help="Print results without writing to Notion")
    args = parser.parse_args()

    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    # Fetch page
    print(f"Fetching page {args.page_id}...")
    page = notion_get(f"pages/{args.page_id}")
    props = page["properties"]

    name = get_text(props.get("Project", {})) or get_text(props.get("Name", {}))
    validation_query = get_text(props.get("Validation Query", {}))
    pain_query = get_text(props.get("Pain/Desire", {}))

    print(f"Project: {name}")
    print(f"Validation Query: {validation_query}")
    print(f"Pain/Desire: {pain_query}")

    if not validation_query:
        print("Error: no Validation Query set on this page", file=sys.stderr)
        sys.exit(1)

    # Run validation
    print("\nRunning validation...")
    report = run_validation(validation_query, pain_query or None)
    if not report:
        sys.exit(1)

    # Extract fields
    claude = report.get("claude_analysis", {})
    rev = report.get("revenue_estimate", {})

    tam_tier = rev.get("tam_tier", "")
    mrr = claude.get("mrr_12mo_estimate") or rev.get("conservative_mrr", "")
    pricing = claude.get("pricing_assessment", "")
    suggested_probability = claude.get("suggested_probability")
    tam_customers = claude.get("tam_customers")
    price_annual = claude.get("price_per_customer_annual")
    value = claude.get("value")
    suggested_value = round(value) if value else None

    print(f"\nResults:")
    print(f"  TAM Tier:             {tam_tier}")
    print(f"  MRR Estimate:         {mrr}")
    print(f"  Pricing:              {pricing}")
    print(f"  Suggested Probability:{suggested_probability}")
    print(f"  Prob reasoning:       {claude.get('probability_reasoning', '')}")
    print(f"  TAM Customers:        {tam_customers}")
    print(f"  Price/Customer/Year:  ${price_annual}")
    print(f"  Value/yr:             ${value}")
    print(f"  Value reasoning:      {claude.get('value_reasoning', '')}")
    print(f"  Suggested Value ($):  ${suggested_value:,}" if suggested_value else "  Suggested Value ($):  n/a")

    if args.dry_run:
        print("\n[dry-run] Skipping Notion update.")
        return

    # Write numeric fields to table
    table_props = {}
    if tam_tier in ("mass", "mid", "niche"):
        table_props["TAM Tier"] = {"select": {"name": tam_tier}}
    if suggested_value is not None:
        table_props["Suggested Value ($)"] = {"number": suggested_value}
    if suggested_probability is not None:
        table_props["Suggested Probability"] = {"number": float(suggested_probability)}
        table_props["Probability"] = {"number": float(suggested_probability)}

    print("\nWriting table fields...")
    notion_patch(f"pages/{args.page_id}", {"properties": table_props})

    # Write text fields to page body
    print("Writing page body...")
    blocks = get_page_blocks(args.page_id)
    remove_existing_validation_section(blocks)
    append_validation_section(args.page_id, report, suggested_probability or 0.1, claude)
    print("Done.")


if __name__ == "__main__":
    main()
