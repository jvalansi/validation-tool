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
PYTHON = sys.executable

NOTION_PROJECTS_DB = "17731083-1fdd-4c06-a3c3-c87aa758703a"


def fetch_top_projects(limit=20):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/databases/{NOTION_PROJECTS_DB}/query",
        data=json.dumps({
            "sorts": [{"property": "ROI", "direction": "descending"}],
            "page_size": limit,
        }).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())

    projects = []
    for page in data["results"]:
        props = page["properties"]
        name = "".join(t["plain_text"] for t in props.get("Project", {}).get("title", []))
        desc = "".join(t["plain_text"] for t in props.get("Description", {}).get("rich_text", []))
        query = "".join(t["plain_text"] for t in props.get("Validation Query", {}).get("rich_text", []))
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
            "subreddits": subreddits,
            "prob": prob,
        })
    return projects


def run_validation(query, subreddits):
    cmd = [PYTHON, VALIDATION_TOOL, "report", "--query", query]
    if subreddits:
        cmd += ["--reddit-subreddits", subreddits]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def calc_new_prob(current_prob, report, project_name, project_desc):
    if not report:
        return current_prob, ""

    prompt = f"""You are evaluating the market validation signals for a software project idea.

Project: {project_name}
Description: {project_desc}

Validation data gathered from multiple sources:
{json.dumps(report["sources"], indent=2)}

Based on this data, classify the probability of commercial success into exactly one of three tiers:

- 0.01 — Moonshot: weak or noisy signals, crowded market, no clear moat or differentiation
- 0.10 — Challenge: real demand exists, but significant competition or execution risk
- 0.99 — Sure thing: exceptional signal, clear unmet need, little competition

Consider:
- Google Trends average interest and direction (growing vs declining demand)
- Hacker News results count and top post engagement (developer interest)
- Reddit discussion volume and relevance of top posts (real user pain points)
- Product Hunt existing products (competition level and market validation)
- Whether signals confirm real demand or just noise
- High competition can mean validated market OR hard to win — use context to judge

Respond with ONLY a JSON object in this exact format:
{{"probability": 0.01|0.10|0.99, "reasoning": "one sentence explanation"}}"""

    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    result = subprocess.run(
        ["/home/ubuntu/.local/bin/claude", "-p", prompt, "--output-format", "json", "--dangerously-skip-permissions"],
        capture_output=True, text=True, timeout=60,
        env=env,
        cwd="/home/ubuntu"
    )
    if result.returncode != 0 or not result.stdout.strip():
        print(f"  Claude error: {result.stderr[:200] or 'no output'}")
        return current_prob, ""

    # claude --output-format json wraps in {"result": "...", ...}
    outer = json.loads(result.stdout)
    inner_text = outer.get("result", "{}")
    # strip markdown code fences if present
    inner_text = inner_text.strip().strip("```json").strip("```").strip()
    inner = json.loads(inner_text)
    new_prob = round(max(0.01, min(0.99, float(inner["probability"]))), 2)
    reasoning = inner.get("reasoning", "")
    print(f"  Reasoning: {reasoning}")
    return new_prob, reasoning


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
                # Parse value and work weeks from surrounding bullets
                value, hours, diff = None, None, 0.4
                for bb in blocks:
                    if bb["type"] == "bulleted_list_item":
                        t = "".join(x.get("plain_text", "") for x in bb["bulleted_list_item"].get("rich_text", []))
                        if "Yearly Revenue" in t:
                            import re
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


def append_validation_section(page_id, report, new_prob, old_prob, reasoning=""):
    if not report:
        return
    gt = report["sources"].get("google_trends", {})
    hn = report["sources"].get("hacker_news", {})
    rd = report["sources"].get("reddit", {})
    ph = report["sources"].get("product_hunt", {})

    gt_line = f"📈 Google Trends: {gt.get('average_interest', 'N/A')}/100 avg, trend {gt.get('trend_direction', 'unknown')}" if "average_interest" in gt else "📈 Google Trends: no data"

    hn_line = f"🟡 Hacker News: {hn.get('total_results', 0)} results"
    if hn.get("top_posts"):
        top = hn["top_posts"][0]
        hn_line += f" — top: \"{top['title']}\" ({top['points']} pts)"

    rd_total = rd.get("total_results", 0)
    rd_line = f"💬 Reddit: {rd_total} results"
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
    prob_note = f"Probability updated: {old_prob*100:.0f}% → {new_prob*100:.0f}%"

    blocks = [
        {"heading_2": {"rich_text": [{"text": {"content": "Validation (Mar 2026)"}}]}},
        {"heading_3": {"rich_text": [{"text": {"content": "Signals"}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": gt_line}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": hn_line}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": rd_line}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": ph_line}}]}},
    ]
    if signals:
        blocks.append({"bulleted_list_item": {"rich_text": [{"text": {"content": "✅ Positive signals: " + ", ".join(signals)}}]}})
    blocks += [
        {"heading_3": {"rich_text": [{"text": {"content": "Verdict"}}]}},
        {"callout": {
            "rich_text": [{"text": {"content": f"{verdict}. {prob_note}."}}],
            "icon": {"type": "emoji", "emoji": "🧪"}
        }},
    ]
    if reasoning:
        blocks.append({"quote": {"rich_text": [{"text": {"content": f"🤖 {reasoning}"}}]}})

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


def process_project(p):
    print(f"\n{'='*60}")
    print(f"Project: {p['name']}")
    print(f"Query: {p['query']}")

    report = run_validation(p["query"], p["subreddits"])
    new_prob, reasoning = calc_new_prob(p["prob"], report, p["name"], p.get("desc", ""))
    print(f"Probability: {p['prob']} → {new_prob}")

    # Update table probability
    notion_patch(f"pages/{p['id']}", {"properties": {"Probability": {"number": new_prob}}})

    # Update page body
    blocks = get_page_blocks(p["id"])
    update_prob_bullet(blocks, new_prob)
    update_callout(blocks, new_prob)
    remove_existing_validation_section(blocks)
    append_validation_section(p["id"], report, new_prob, p["prob"], reasoning)

    summary = report.get("summary", {}) if report else {}
    print(f"Verdict: {summary.get('verdict', 'N/A')}")
    print(f"Signals: {summary.get('positive_signals', [])}")


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
