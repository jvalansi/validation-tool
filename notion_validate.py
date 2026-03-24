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
    pricing = claude.get("pricing_recommendation", "")
    signal = claude.get("roi_verdict", "")

    print(f"\nResults:")
    print(f"  TAM Tier:    {tam_tier}")
    print(f"  MRR Estimate: {mrr}")
    print(f"  Pricing:     {pricing}")
    print(f"  Market Signal: {signal}")

    if args.dry_run:
        print("\n[dry-run] Skipping Notion update.")
        return

    # Write back to Notion
    update = {"properties": {}}
    if tam_tier in ("mass", "mid", "niche"):
        update["properties"]["TAM Tier"] = {"select": {"name": tam_tier}}
    if mrr:
        update["properties"]["MRR Estimate"] = {"rich_text": [{"text": {"content": mrr}}]}
    if pricing:
        update["properties"]["Pricing Recommendation"] = {"rich_text": [{"text": {"content": pricing[:2000]}}]}
    if signal in ("strong", "moderate", "weak", "unclear"):
        update["properties"]["Market Signal"] = {"select": {"name": signal}}

    print("\nWriting to Notion...")
    notion_patch(f"pages/{args.page_id}", update)
    print("Done.")


if __name__ == "__main__":
    main()
