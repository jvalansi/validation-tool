#!/usr/bin/env python3
"""
Phase 2: Launch campaign for a validated Notion project.

Usage:
  python phase2.py <notion-page-id> [--budget 100] [--days 7] [--dry-run]

Steps:
  1. Deploy landing page (GitHub Pages)   ← implemented
  2. Reddit posts                         ← stub
  3. HN Show HN post                      ← stub
  4. Google Ads                           ← stub
  5. Email capture follow-up             ← stub
  6. Report signups                       ← stub
"""

import argparse
import json
import os
import sys
import urllib.request

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"


def notion_get(path):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
        },
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


def step1_landing_page(project_name, description, pain_desire, price_per_year, dry_run):
    from phase2.landing import deploy_landing_page
    print(f"\n[Step 1] Deploying landing page for: {project_name}")
    result = deploy_landing_page(
        project_name=project_name,
        description=description,
        pain_desire=pain_desire,
        price_per_year=price_per_year,
        form_url=None,
        dry_run=dry_run,
    )
    return result


def step2_reddit(project_name, dry_run):
    print("\n[Step 2] Reddit posts — stub (not yet implemented)")
    return {"status": "stub"}


def step3_hn(project_name, dry_run):
    print("\n[Step 3] HN Show HN post — stub (not yet implemented)")
    return {"status": "stub"}


def step4_ads(project_name, budget, days, dry_run):
    print("\n[Step 4] Google Ads — stub (not yet implemented)")
    return {"status": "stub"}


def step5_email(project_name, dry_run):
    print("\n[Step 5] Email capture follow-up — stub (not yet implemented)")
    return {"status": "stub"}


def step6_report(project_name, dry_run):
    print("\n[Step 6] Report signups — stub (not yet implemented)")
    return {"status": "stub"}


def main():
    parser = argparse.ArgumentParser(description="Phase 2 launch campaign for a Notion project")
    parser.add_argument("page_id", help="Notion page ID")
    parser.add_argument("--budget", type=float, default=100, help="Ad budget in USD (default: 100)")
    parser.add_argument("--days", type=int, default=7, help="Campaign duration in days (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Print output without deploying or posting")
    args = parser.parse_args()

    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    # Fetch Notion page
    print(f"Fetching Notion page {args.page_id}...")
    page = notion_get(f"pages/{args.page_id}")
    props = page["properties"]

    project_name = get_text(props.get("Project", {})) or get_text(props.get("Name", {}))
    description = get_text(props.get("Description", {}))
    pain_desire = get_text(props.get("Pain/Desire", {}))

    # Price/Customer/yr ($) is a number property
    price_prop = props.get("Price/Customer/yr ($)", {})
    price_per_year = price_prop.get("number") if price_prop else None

    print(f"Project:        {project_name}")
    print(f"Description:    {description}")
    print(f"Pain/Desire:    {pain_desire}")
    print(f"Price/yr:       {price_per_year}")

    if not project_name:
        print("Error: no Project/Name on this Notion page", file=sys.stderr)
        sys.exit(1)

    results = {}

    # Step 1: Landing page
    landing_result = step1_landing_page(project_name, description, pain_desire, price_per_year, args.dry_run)
    results["landing"] = landing_result

    # Steps 2-6: stubs
    results["reddit"] = step2_reddit(project_name, args.dry_run)
    results["hn"] = step3_hn(project_name, args.dry_run)
    results["ads"] = step4_ads(project_name, args.budget, args.days, args.dry_run)
    results["email"] = step5_email(project_name, args.dry_run)
    results["report"] = step6_report(project_name, args.dry_run)

    print("\n--- Results ---")
    print(json.dumps(results, indent=2))

    # Update Notion with landing page URL if deployed
    if not args.dry_run and landing_result.get("status") == "deployed":
        pages_url = landing_result.get("pages_url", "")
        if pages_url:
            try:
                notion_patch(f"pages/{args.page_id}", {
                    "properties": {
                        "Landing Page URL": {
                            "rich_text": [{"text": {"content": pages_url}}]
                        }
                    }
                })
                print(f"\nUpdated Notion with Landing Page URL: {pages_url}")
            except Exception:
                # Property may not exist in DB schema — silently skip
                pass


if __name__ == "__main__":
    main()
