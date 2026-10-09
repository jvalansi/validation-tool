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
from datetime import date

from validation_tool import merge_competitors, round_oom


NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"
VALIDATION_TOOL = os.path.join(os.path.dirname(__file__), "validation_tool.py")
PYTHON = "/home/ubuntu/miniconda3/bin/python"
EXIT_SEARCH_REFUSED = 3  # same as validation_tool.EXIT_SEARCH_REFUSED
REVIEWED_FIELDS = ("TAM Customers", "TAM Sourced", "Price/Customer/yr ($)", "Price Sourced", "Competition", "Probability")


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
        t = b["type"]
        if t == "heading_2":  # sections are heading_2; the Validation section ends at the next one (e.g. Spec)
            text = "".join(x.get("plain_text", "") for x in b.get(t, {}).get("rich_text", []))
            found = "Validation" in text
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
        if "average_interest" in gt else "📈 Google Trends: skipped" if gt.get("skipped") else "📈 Google Trends: no data"
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
        {"heading_2": {"rich_text": [{"text": {"content": f"Validation ({date.today():%b %Y})"}}]}},
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
        tam_customers = claude.get("tam_customers")
        price_annual = claude.get("price_per_customer_annual")
        key_risks = claude.get("key_risks", [])
        key_opportunities = claude.get("key_opportunities", [])

        if prob_reasoning:
            blocks.append({"quote": {"rich_text": [{"text": {"content": f"🎲 {prob_reasoning}"}}]}})
        if value_reasoning:
            blocks.append({"quote": {"rich_text": [{"text": {"content": f"💰 {value_reasoning}"}}]}})
        if tam:
            blocks.append({"heading_3": {"rich_text": [{"text": {"content": "Market Analysis"}}]}})
            blocks.append({"paragraph": {"rich_text": [{"text": {"content": tam}}]}})
        if tam_customers is not None:
            src = claude.get("tam_source")
            blocks.append({"bulleted_list_item": {"rich_text": [{"text": {"content": f"👥 TAM: ~{tam_customers:,} customers " + (
                f"= {claude.get('tam_source_quote')} {claude.get('customer_group')} ({src}) × {claude.get('tam_share')}: {claude.get('tam_share_reason')}" if src else
                f"(assumed: Claude's guess of {claude.get('tam_guess') or tam_customers:,} ÷ 10, since guesses ran a median 25× above sourced counts)")}}]}})
        if claude.get("competitors"):
            blocks.append({"bulleted_list_item": {"rich_text": [{"text": {"content": f"🏁 Competitors ({report.get('summary', {}).get('competition')}): "
                + ", ".join(c["name"] for c in claude["competitors"])}}]}})
        if price_annual is not None:
            psrc = claude.get("price_source")
            one_time = claude.get("price_one_time")
            blocks.append({"bulleted_list_item": {"rich_text": [{"text": {"content": (
                f"💵 Price: ~${one_time:,.0f} one-time, counted as ${price_annual:,.0f}/yr " if one_time else f"💵 Price: ~${price_annual}/yr per customer ") + (
                f"(source: \"{claude.get('price_source_quote')}\" {psrc})" if psrc else "(assumed: no comparable vendor price found)")}}]}})
        if pricing:
            blocks.append({"bulleted_list_item": {"rich_text": [{"text": {"content": f"💰 Pricing: {pricing}"}}]}})
        if key_risks:
            blocks.append({"heading_3": {"rich_text": [{"text": {"content": "Risks"}}]}})
            for risk in key_risks:
                blocks.append({"bulleted_list_item": {"rich_text": [{"text": {"content": f"⚠️ {risk}"}}]}})
        if key_opportunities:
            blocks.append({"heading_3": {"rich_text": [{"text": {"content": "Opportunities"}}]}})
            for opp in key_opportunities:
                blocks.append({"bulleted_list_item": {"rich_text": [{"text": {"content": f"✅ {opp}"}}]}})

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


def reuse_prior_tam(claude, props):
    """Whether a count is found varies run to run, so a run that finds none keeps the last sourced
    TAM (population x share stored on the page) instead of falling back to Claude's guess."""
    pop = (props.get("TAM Population") or {}).get("number")
    share = (props.get("TAM Share") or {}).get("number")
    if claude.get("tam_sourced") or not pop or not share:
        return
    claude.update(tam_sourced=True, tam_reused=True, tam_population=pop, tam_customers=round_oom(pop * share),
                  tam_share=f"{share:.1%}".replace(".0%", "%"), tam_source=(props.get("TAM Source") or {}).get("url"),
                  tam_source_quote=get_text(props.get("TAM Source Quote", {})), customer_group=get_text(props.get("Customer Group", {})),
                  tam_share_reason="kept from an earlier run")


def reuse_prior_competitors(report, claude, props):
    """Competitors cited on earlier runs stay counted, so a search that misses one doesn't lower the grade."""
    stored = "".join(t.get("plain_text", "") for t in (props.get("Competitors") or {}).get("rich_text", []))
    if claude and stored:
        merge_competitors(report, claude, json.loads(stored))


def run_validation(query, pain_query=None, trends_query=None, skip_trends=False, require_brave=False):
    cmd = [PYTHON, VALIDATION_TOOL, "report", "--query", query] + (["--skip-trends"] if skip_trends else []) + (
        ["--require-brave"] if require_brave else [])
    if pain_query:
        cmd += ["--pain-query", pain_query, "--assume-tech-exists"]
    if trends_query:
        cmd += ["--trends-query", trends_query]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 3 Claude calls + page fetches
    if result.returncode == EXIT_SEARCH_REFUSED:
        print(result.stderr[-300:], file=sys.stderr)
        sys.exit(EXIT_SEARCH_REFUSED)
    if result.returncode != 0:
        print(f"Validation error: {result.stderr[:200]}", file=sys.stderr)
        return None
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description="Validate a Notion project and write results back")
    parser.add_argument("page_id", help="Notion page ID")
    parser.add_argument("--dry-run", action="store_true", help="Print results without writing to Notion")
    parser.add_argument("--skip-trends", action="store_true",
                        help="Skip Google Trends and leave Trends Interest, TAM Tier and Market Signal as they are")
    parser.add_argument("--require-brave", action="store_true",
                        help=f"Exit {EXIT_SEARCH_REFUSED} without writing if Brave refuses a search")
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
    trends_query = get_text(props.get("Trends Query", {}))

    print(f"Project: {name}")
    print(f"Validation Query: {validation_query}")
    print(f"Pain/Desire: {pain_query}")

    if not validation_query:
        print("Error: no Validation Query set on this page", file=sys.stderr)
        sys.exit(1)

    # Run validation
    print("\nRunning validation...")
    report = run_validation(validation_query, pain_query or None, trends_query or None, args.skip_trends, args.require_brave)
    if not report:
        sys.exit(1)

    # Extract fields
    claude = report.get("claude_analysis", {})
    reuse_prior_tam(claude, props)
    reuse_prior_competitors(report, claude, props)
    rev = report.get("revenue_estimate", {})
    sources = report.get("sources", {})

    tam_tier = rev.get("tam_tier", "")
    mrr = claude.get("mrr_12mo_estimate") or rev.get("conservative_mrr", "")
    pricing = claude.get("pricing_assessment", "")
    suggested_probability = claude.get("suggested_probability")
    tam_customers = claude.get("tam_customers")
    price_annual = claude.get("price_per_customer_annual")
    value = claude.get("value")
    suggested_value = round(value) if value else None

    trends_avg = sources.get("google_trends", {}).get("average_interest")
    hn_results = sources.get("hacker_news", {}).get("total_results")
    reddit_results = sources.get("reddit", {}).get("total_results")
    ph_products = sources.get("product_hunt", {}).get("existing_products")

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

    # Derive market signal from signal count
    signal_count = report.get("summary", {}).get("signal_count", 0)
    if signal_count >= 3:
        market_signal = "strong"
    elif signal_count >= 1:
        market_signal = "moderate"
    else:
        market_signal = "weak"

    # Write numeric/select fields to table
    table_props = {}
    if tam_tier in ("mass", "mid", "niche") and not args.skip_trends:  # tier comes from Trends
        table_props["TAM Tier"] = {"select": {"name": tam_tier}}
    if suggested_value is not None:
        table_props["Value ($)"] = {"number": suggested_value}
    if suggested_probability is not None:
        table_props["Probability"] = {"number": float(suggested_probability)}
    if not args.skip_trends:  # without Trends the signal count is missing its search-volume signals
        table_props["Market Signal"] = {"select": {"name": market_signal}}
    if claude.get("competitors"):
        stored = json.dumps(claude["competitors"], ensure_ascii=False)
        table_props["Competitors"] = {"rich_text": [{"text": {"content": stored[i:i + 2000]}} for i in range(0, len(stored), 2000)]}
    competition = report.get("summary", {}).get("competition")
    if competition:
        table_props["Competition"] = {"select": {"name": competition}}
    if trends_avg is not None:
        table_props["Trends Interest"] = {"number": float(trends_avg)}
    if hn_results is not None:
        table_props["HN Results"] = {"number": int(hn_results)}
    if reddit_results is not None:
        table_props["Reddit Results"] = {"number": int(reddit_results)}
    if ph_products is not None:
        table_props["PH Products"] = {"number": int(ph_products)}
    if tam_customers is not None:
        table_props["TAM Customers"] = {"number": int(tam_customers)}
    table_props["TAM Sourced"] = {"checkbox": bool(claude.get("tam_sourced"))}
    if claude.get("tam_sourced") and not claude.get("tam_reused"):
        table_props.update({
            "TAM Population": {"number": claude["tam_population"]},
            "TAM Share": {"number": float(claude["tam_share"].rstrip("%")) / 100},
            "TAM Source": {"url": claude.get("tam_source")},
            "TAM Source Quote": {"rich_text": [{"text": {"content": str(claude.get("tam_source_quote") or "")[:200]}}]},
            "Customer Group": {"rich_text": [{"text": {"content": str(claude.get("customer_group") or "")[:200]}}]},
        })
    table_props["Price Sourced"] = {"checkbox": bool(claude.get("price_sourced"))}
    if price_annual is not None:
        table_props["Price/Customer/yr ($)"] = {"number": float(price_annual)}

    print("\nWriting table fields...")
    if (props.get("Reviewed") or {}).get("checkbox"):  # set by hand-review; a run's estimates don't replace it
        for k in REVIEWED_FIELDS:
            table_props.pop(k, None)
    notion_patch(f"pages/{args.page_id}", {"properties": table_props})

    # Write text fields to page body
    print("Writing page body...")
    blocks = get_page_blocks(args.page_id)
    remove_existing_validation_section(blocks)
    append_validation_section(args.page_id, report, suggested_probability or 0.1, claude)
    from datetime import datetime, timezone  # stamped last: revalidate_all.py resumes from ideas without it
    notion_patch(f"pages/{args.page_id}", {"properties": {"Validated": {"date": {
        "start": datetime.now(timezone.utc).isoformat(timespec="seconds")}}}})
    print("Done.")


if __name__ == "__main__":
    main()
