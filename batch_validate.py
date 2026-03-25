#!/usr/bin/env python3
"""
Batch validate Notion projects and update pages with results.
"""
import json
import os
import subprocess
import sys
import urllib.request

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_VERSION = "2022-06-28"
VALIDATION_TOOL = os.path.join(os.path.dirname(__file__), "validation_tool.py")
PYTHON = "/home/ubuntu/miniconda3/bin/python"

NOTION_PROJECTS_DB = "17731083-1fdd-4c06-a3c3-c87aa758703a"
VALIDATED_IDS_FILE = os.path.join(os.path.dirname(__file__), "validated_ids.json")


def load_validated_ids():
    if os.path.exists(VALIDATED_IDS_FILE):
        with open(VALIDATED_IDS_FILE) as f:
            return set(json.load(f))
    return set()


def save_validated_id(page_id):
    ids = load_validated_ids()
    ids.add(page_id)
    with open(VALIDATED_IDS_FILE, "w") as f:
        json.dump(list(ids), f)


def fetch_top_projects(limit=20):
    validated = load_validated_ids()
    all_pages = []
    cursor = None

    while len(all_pages) < 200:  # safety cap
        body = {"sorts": [{"property": "ROI", "direction": "descending"}], "page_size": 20}
        if cursor:
            body["start_cursor"] = cursor
        req = urllib.request.Request(
            f"https://api.notion.com/v1/databases/{NOTION_PROJECTS_DB}/query",
            data=json.dumps(body).encode(),
            method="POST",
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        all_pages.extend(data["results"])
        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]

    projects = []
    for page in all_pages:
        if page["id"] in validated:
            continue
        props = page["properties"]
        name = "".join(t["plain_text"] for t in props.get("Project", {}).get("title", []))
        desc = "".join(t["plain_text"] for t in props.get("Description", {}).get("rich_text", []))
        query = "".join(t["plain_text"] for t in props.get("Validation Query", {}).get("rich_text", []))
        pain_query = "".join(t["plain_text"] for t in props.get("Pain/Desire", {}).get("rich_text", []))
        subreddits = "".join(t["plain_text"] for t in props.get("Subreddits", {}).get("rich_text", []))
        prob = props.get("Probability", {}).get("number") or 0.1
        if not query:
            print(f"Skipping '{name}' — no validation query")
            continue
        projects.append({
            "id": page["id"],
            "name": name,
            "desc": desc,
            "query": query,
            "pain_query": pain_query,
            "subreddits": subreddits,
            "prob": prob,
        })
        if len(projects) >= limit:
            break
    return projects


def run_validation(query, pain_query=None, subreddits=None, trends_query=None):
    cmd = [PYTHON, VALIDATION_TOOL, "report", "--query", query]
    if pain_query:
        cmd += ["--pain-query", pain_query, "--assume-tech-exists"]
    if subreddits:
        cmd += ["--reddit-subreddits", subreddits]
    if trends_query:
        cmd += ["--trends-query", trends_query]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        print(f"  Validation error: {result.stderr[:200]}")
        return None
    return json.loads(result.stdout)


def notion_patch(path, body):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        data=json.dumps(body).encode(),
        method="PATCH",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def get_page_blocks(page_id):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers={"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": NOTION_VERSION},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read()).get("results", [])


def update_prob_bullet(blocks, new_prob):
    for b in blocks:
        if b["type"] == "bulleted_list_item":
            text = "".join(x.get("plain_text", "") for x in b["bulleted_list_item"].get("rich_text", []))
            if "Probability of success" in text:
                notion_patch(f"blocks/{b['id']}", {
                    "bulleted_list_item": {"rich_text": [{"text": {"content": f"🎲 Probability of success: {new_prob*100:.2f}%"}}]}
                })
                return


def update_callout(blocks, new_prob):
    for b in blocks:
        if b["type"] == "callout":
            text = "".join(x.get("plain_text", "") for x in b["callout"].get("rich_text", []))
            if "ROI score" in text:
                import re
                value, hours, diff = None, None, 0.4
                for bb in blocks:
                    if bb["type"] == "bulleted_list_item":
                        t = "".join(x.get("plain_text", "") for x in bb["bulleted_list_item"].get("rich_text", []))
                        if "Yearly Revenue" in t:
                            m = re.search(r'\$([\d,]+)', t)
                            if m:
                                value = int(m.group(1).replace(",", ""))
                        if "work hours" in t.lower() or "estimated work" in t.lower():
                            m = re.search(r'(\d+)h', t)
                            if m:
                                hours = int(m.group(1))
                if value and hours:
                    roi = (value * new_prob) / (hours * diff)
                    notion_patch(f"blocks/{b['id']}", {
                        "callout": {
                            "rich_text": [{"text": {"content": f"ROI score: {roi:.1f}  =  (${value:,} × {new_prob*100:.2f}%) ÷ ({hours}h × {int(diff*100)}% difficulty)"}}],
                            "icon": {"type": "emoji", "emoji": "💡"}
                        }
                    })
                return


def delete_block(block_id):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/blocks/{block_id}",
        method="DELETE",
        headers={"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": NOTION_VERSION},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


def remove_existing_validation_section(blocks):
    """Delete all blocks from the Validation heading onwards."""
    found = False
    for b in blocks:
        if not found:
            t = b["type"]
            text = "".join(x.get("plain_text", "") for x in b.get(t, {}).get("rich_text", []))
            if t == "heading_2" and "Validation" in text:
                found = True
        if found:
            try:
                delete_block(b["id"])
            except Exception:
                pass


def append_validation_section(page_id, report, new_prob, old_prob, claude):
    if not report:
        return
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
    prob_note = f"Probability: {old_prob*100:.0f}% → {new_prob*100:.0f}%"

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
            "rich_text": [{"text": {"content": f"{verdict}. {prob_note}."}}],
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


def update_notion_table(page_id, new_prob, claude, rev, report):
    """Write all structured fields back to the Notion table."""
    props = {"Probability": {"number": new_prob}}

    if claude:
        value = claude.get("value")
        if value:
            props["Value ($)"] = {"number": round(value)}
        tam_customers = claude.get("tam_customers")
        if tam_customers is not None:
            props["TAM Customers"] = {"number": int(tam_customers)}
        price_annual = claude.get("price_per_customer_annual")
        if price_annual is not None:
            props["Price/Customer/yr ($)"] = {"number": float(price_annual)}

    if rev:
        tam_tier = rev.get("tam_tier", "")
        if tam_tier in ("mass", "mid", "niche"):
            props["TAM Tier"] = {"select": {"name": tam_tier}}

    if report:
        gt = report.get("sources", {}).get("google_trends", {})
        hn = report.get("sources", {}).get("hacker_news", {})
        rd = report.get("sources", {}).get("reddit", {})
        ph = report.get("sources", {}).get("product_hunt", {})
        if "average_interest" in gt:
            props["Trends Interest"] = {"number": float(gt["average_interest"])}
        hn_count = hn.get("total_results")
        if hn_count is not None:
            props["HN Results"] = {"number": int(hn_count)}
        rd_count = rd.get("total_results")
        if rd_count is not None:
            props["Reddit Results"] = {"number": int(rd_count)}
        ph_count = ph.get("existing_products")
        if ph_count is not None and ph_count >= 0:
            props["PH Products"] = {"number": int(ph_count)}

        signal_count = report.get("summary", {}).get("signal_count", 0)
        if signal_count >= 3:
            props["Market Signal"] = {"select": {"name": "strong"}}
        elif signal_count >= 1:
            props["Market Signal"] = {"select": {"name": "moderate"}}
        else:
            props["Market Signal"] = {"select": {"name": "weak"}}

    notion_patch(f"pages/{page_id}", {"properties": props})


def process_project(p):
    print(f"\n{'='*60}")
    print(f"Project: {p['name']}")
    print(f"Query: {p['query']}")

    report = run_validation(p["query"], p.get("pain_query") or None, p.get("subreddits") or None, p.get("trends_query") or None)
    if not report:
        print("  No report — skipping")
        return

    claude = report.get("claude_analysis", {})
    rev = report.get("revenue_estimate", {})

    new_prob = float(claude.get("suggested_probability") or p["prob"])
    new_prob = round(max(0.01, min(0.99, new_prob)), 2)

    print(f"  Probability:      {p['prob']} → {new_prob}")
    print(f"  TAM Customers:    {claude.get('tam_customers', 'n/a')}")
    print(f"  Price/yr:         ${claude.get('price_per_customer_annual', 'n/a')}")
    print(f"  Value/yr:         ${claude.get('value', 'n/a')}")
    print(f"  Value reasoning:  {claude.get('value_reasoning', '')}")
    print(f"  Prob reasoning:   {claude.get('probability_reasoning', '')}")

    # Update table
    update_notion_table(p["id"], new_prob, claude, rev, report)

    # Update page body
    blocks = get_page_blocks(p["id"])
    update_prob_bullet(blocks, new_prob)
    update_callout(blocks, new_prob)
    remove_existing_validation_section(blocks)
    append_validation_section(p["id"], report, new_prob, p["prob"], claude)

    save_validated_id(p["id"])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    projects = fetch_top_projects(limit=args.limit)
    print(f"Fetched {len(projects)} projects to validate")
    for p in projects:
        try:
            process_project(p)
        except Exception as e:
            print(f"ERROR on {p['name']}: {e}")
    print("\n✅ Done")
