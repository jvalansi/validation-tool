#!/usr/bin/env python3
"""
Phase 2: Launch campaign for a validated Notion project.

Usage:
  python phase2.py <notion-page-id> [--budget 100] [--days 7] [--dry-run]
  python phase2.py monitor [--dry-run]

Steps:
  1. Deploy landing page (GitHub Pages)   ← implemented
  2. Tally signup form                    ← implemented
  3. Daily monitor                        ← implemented
  4. Google Ads                           ← stub
  5. Outreach drafts                      ← stub
  6. Day 7 decision                       ← stub
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


def generate_subtitle(project_name, description, pain_desire):
    """Use Claude to distill description into a one-line subtitle."""
    claude_path = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    if not os.path.exists(claude_path):
        return description

    prompt = f"""Write a single subtitle sentence for a landing page. Max 15 words. No jargon.
It should explain what the product does and who it's for, in plain English.

Project: {project_name}
Description: {description}
Pain: {pain_desire}

Return only the subtitle text, nothing else."""

    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        result = subprocess.run(
            [claude_path, "-p", prompt, "--output-format", "json", "--dangerously-skip-permissions"],
            capture_output=True, text=True, timeout=30,
            env=env, cwd="/home/ubuntu"
        )
        if result.returncode == 0 and result.stdout.strip():
            outer = json.loads(result.stdout)
            return outer.get("result", "").strip().strip('"')
    except Exception:
        pass
    return description


def generate_headline(project_name, description, pain_desire):
    """Use Claude to distill pain/desire into a punchy 6-10 word hero headline."""
    claude_path = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    if not os.path.exists(claude_path):
        return pain_desire

    prompt = f"""Write a single hero headline for a landing page. 6-10 words max. No punctuation at the end.
It should express the core pain or desire — something a visitor instantly recognizes as their problem.

Project: {project_name}
Description: {description}
Pain/desire research: {pain_desire}

Return only the headline text, nothing else."""

    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        result = subprocess.run(
            [claude_path, "-p", prompt, "--output-format", "json", "--dangerously-skip-permissions"],
            capture_output=True, text=True, timeout=30,
            env=env, cwd="/home/ubuntu"
        )
        if result.returncode == 0 and result.stdout.strip():
            outer = json.loads(result.stdout)
            return outer.get("result", "").strip().strip('"')
    except Exception:
        pass
    return pain_desire


def generate_features(project_name, description, pain_desire):
    """Use Claude to generate 3 feature cards for the landing page."""
    claude_path = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    if not os.path.exists(claude_path):
        return None

    prompt = f"""Generate exactly 3 short feature/benefit cards for a landing page.

Project: {project_name}
Description: {description}
Pain it solves: {pain_desire}

Return JSON array of 3 objects with keys:
- "icon_key": one of: chart, zap, shield, cpu, eye, layers, dollar, code, arrow
- "title": 3-5 word feature title
- "body": one sentence benefit (max 12 words)

Return only valid JSON array, no markdown."""

    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        result = subprocess.run(
            [claude_path, "-p", prompt, "--output-format", "json", "--dangerously-skip-permissions"],
            capture_output=True, text=True, timeout=30,
            env=env, cwd="/home/ubuntu"
        )
        if result.returncode == 0 and result.stdout.strip():
            outer = json.loads(result.stdout)
            text = outer.get("result", "").strip()
            if text.startswith("```"):
                text = "\n".join(text.split("\n")[1:]).rsplit("```", 1)[0].strip()
            return json.loads(text)
    except Exception:
        pass
    return None


def step1_landing_page(project_name, description, pain_desire, price_per_year, dry_run):
    from phase2.landing import deploy_landing_page
    print(f"\n[Step 1] Generating copy...")
    headline = generate_headline(project_name, description, pain_desire)
    print(f"  Headline: {headline}")
    subtitle = generate_subtitle(project_name, description, pain_desire)
    print(f"  Subtitle: {subtitle}")
    features = generate_features(project_name, description, pain_desire)
    if features:
        print(f"  Got {len(features)} feature cards from Claude")

    print(f"[Step 2] Creating Tally signup form...")
    form_result = step2_tally_form(project_name, pain_desire, price_per_year, dry_run)
    embed_url = form_result.get("embed_url")

    print(f"[Step 1] Deploying landing page for: {project_name}")
    result = deploy_landing_page(
        project_name=project_name,
        description=subtitle,
        pain_desire=headline,
        price_per_year=price_per_year,
        form_url=embed_url,
        features=features,
        dry_run=dry_run,
    )
    result["form"] = form_result

    # Register campaign for daily monitoring
    if not dry_run and result.get("status") == "deployed" and form_result.get("form_id"):
        from phase2.monitor import register_campaign
        register_campaign(
            project_name=project_name,
            form_id=form_result["form_id"],
            pages_url=result["pages_url"],
        )
        print(f"  Campaign registered for daily monitoring")

    return result


def step2_tally_form(project_name, pain_desire, price_per_year, dry_run):
    from phase2.forms import create_signup_form
    if dry_run:
        return {"status": "dry_run", "embed_url": None}
    result = create_signup_form(project_name, pain_desire, price_per_year)
    print(f"  Form: {result['form_url']}")
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
    parser.add_argument("page_id", nargs="?", help="Notion page ID, or 'monitor' to run daily monitor")
    parser.add_argument("--budget", type=float, default=100, help="Ad budget in USD (default: 100)")
    parser.add_argument("--days", type=int, default=7, help="Campaign duration in days (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Print output without deploying or posting")
    args = parser.parse_args()

    if args.page_id == "monitor":
        from phase2.monitor import run_monitor
        run_monitor(dry_run=args.dry_run)
        return

    if not args.page_id:
        parser.error("page_id is required (or use 'monitor')")

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
