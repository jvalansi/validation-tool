#!/usr/bin/env python3
"""
Score a Notion idea the way a hand review does: one Claude Code session reads the whole row, searches the
web as it needs, compares against hand-reviewed rows, and fills TAM, price, competition and probability.
Code then snaps every number to its allowed steps and drops any source whose quote isn't on the cited page.

Usage:
  python agent_review.py <page-id>            # review and write to Notion
  python agent_review.py <page-id> --dry-run  # print, don't write
  python agent_review.py --blind-test [N]     # re-score N hand-reviewed rows without their values; compare
"""

import argparse
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

from notion_validate import (NOTION_TOKEN, get_page_blocks, get_text, notion_get, notion_patch,
                             remove_existing_validation_section)
from validation_tool import COMPETITION_LEVELS, _extract_prices, _page_text, round_oom

NOTION_DB = "17731083-1fdd-4c06-a3c3-c87aa758703a"
PROBABILITIES = (0.001, 0.01, 0.03, 0.1, 0.3)
REFERENCE_ROWS = 12

RUBRIC = """Fill in this idea's row for an ROI ranking: ROI = TAM x price x market share x 10 years x probability / cost of the work weeks.
Use web search and page fetches as much as you need: look up real counts, real competitor prices, and who already sells this.
Everything is per the idea as described; if it is a personal goal or research question, score it as the product it could become.

- tam: number of customers who would plausibly pay for this kind of product (not everyone in the group). Find a sourced
  count of the population (population, population_source_url, population_quote: the count exactly as written on that page)
  and pick the share of it that would pay (share: 1, 0.1, 0.01 or 0.001). If you find no count, give tam directly.
- price: revenue YOU keep per customer per year in USD: for a marketplace or payments product, the take rate x what they
  spend, not the spend. price_type "one_time" for a one-off purchase (give the one-time price), else "recurring".
  If a real competitor's price backs it: price_source_url and price_quote (the price exactly as written on that page).
- competition: direct rivals only, i.e. products these buyers would compare against this one (adjacent markets don't count):
    "dominant" a big-tech product or a rival that raised >= $100M owns the category; "crowded" 5+ rivals, or a funded one
    among several; "funded" a rival raised >= $10M; "contested" 2-4 small rivals; "open" 1; "none_found" none.
  competitors: up to 8 of them as {{"name", "url", "why": what it sells, "funding_usd" or null}}.
- probability: chance a solo founder gets this to paying customers at the share competition allows. One of:
    0.001 research idea or needs a breakthrough; 0.01 needs a real edge (e.g. trading alpha), faces a category owner, or has
    no defined product; 0.03 crowded or hard to sell (consumer distribution, two-sided marketplace, regulation, hardware);
    0.1 cheap to build and sell, or already built; 0.3 only with strong evidence such as paying users.
- work_weeks: solo-founder weeks still needed to reach a sellable version (only if asked below).
- reasons: one short clause per field (tam, price, competition, probability) saying why.

Hand-reviewed rows to calibrate against (name | tam | price | competition | probability | note):
{references}

The idea:
{idea}

Return only JSON: {{"population": int or null, "population_source_url": str or null, "population_quote": str or null,
"share": number or null, "tam": int, "price": number, "price_type": "one_time" or "recurring", "price_source_url": str or null,
"price_quote": str or null, "competition": str, "competitors": [...], "probability": number, "work_weeks": int or null,
"reasons": {{"tam": str, "price": str, "competition": str, "probability": str}}}}"""


def query_db(body):
    req = urllib.request.Request(f"https://api.notion.com/v1/databases/{NOTION_DB}/query", json.dumps(body).encode(),
                                 {"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": "2022-06-28",
                                  "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["results"]


def reviewed_rows():
    return [p for p in query_db({"page_size": 100, "filter": {"and": [
        {"property": "Reviewed", "checkbox": {"equals": True}},
        {"property": "TAM Customers", "number": {"is_not_empty": True}}]}})]


def reference_lines(rows, exclude=None):
    """A spread of hand-reviewed rows, from the top of the ranking to the bottom."""
    rows = sorted((p for p in rows if p["id"] != exclude), key=lambda p: -(p["properties"]["ROI"]["formula"].get("number") or 0))
    step = max(1, len(rows) // REFERENCE_ROWS)
    out = []
    for p in rows[::step][:REFERENCE_ROWS]:
        r = p["properties"]
        out.append(f"- {get_text(r['Project'])[:60]}: {get_text(r['Description'])[:120]} | {r['TAM Customers']['number']:,} | "
                   f"${r['Price/Customer/yr ($)']['number']} | {r['Competition']['select']['name']} | "
                   f"{r['Probability']['number']} | {get_text(r['Review Note'])[:160]}")
    return "\n".join(out)


def ask_agent(prompt, timeout=900):
    claude = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    result = subprocess.run([claude, "-p", prompt, "--output-format", "json", "--allowedTools", "WebSearch,WebFetch"],
                            capture_output=True, text=True, timeout=timeout, env=env, cwd="/tmp")
    text = json.loads(result.stdout).get("result", "")
    return json.loads(text[text.find("{"):text.rfind("}") + 1])


def page_has(url, quote):
    """The quote (whitespace-insensitive) is in the page's visible text."""
    if not (url and quote):
        return False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (validation-tool)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            text = _page_text(resp.read(2_000_000).decode("utf-8", "ignore"))
    except Exception:
        return False
    squash = lambda t: re.sub(r"\s+", "", str(t).lower())
    return squash(quote) in squash(text)


def snap(a, check=page_has):
    """Agent output -> the row's values: powers of 10, allowed steps, and sources only when the quote is on the page."""
    pop, share = a.get("population"), a.get("share")
    tam_sourced = bool(isinstance(pop, (int, float)) and pop > 0 and share in (1, 0.1, 0.01, 0.001)
                       and check(a.get("population_source_url"), a.get("population_quote")))
    tam = round_oom(pop * share) if tam_sourced else round_oom(max(float(a.get("tam") or 1), 1))
    price = float(a.get("price") or 0)
    quote = a.get("price_quote")
    price_sourced = bool(price > 0 and _extract_prices([str(quote or "")]) and check(a.get("price_source_url"), quote))
    one_time = a.get("price_type") == "one_time"
    annual = max(round_oom(price) / 10 if one_time else round_oom(price), 1) if price > 0 else 1  # Value counts 10 years
    prob = min(PROBABILITIES, key=lambda p: abs(math.log10(p) - math.log10(max(float(a.get("probability") or 0.01), 1e-4))))
    comp = a.get("competition") if a.get("competition") in COMPETITION_LEVELS else "none_found"
    return {"tam": tam, "tam_sourced": tam_sourced, "population": pop if tam_sourced else None, "share": share if tam_sourced else None,
            "tam_source": a.get("population_source_url") if tam_sourced else None,
            "tam_quote": a.get("population_quote") if tam_sourced else None,
            "price": int(annual) if annual >= 1 else annual, "price_one_time": round_oom(price) if one_time and price > 0 else None,
            "price_sourced": price_sourced, "price_source": a.get("price_source_url") if price_sourced else None,
            "price_quote": quote if price_sourced else None, "competition": comp,
            "competitors": [c for c in a.get("competitors") or [] if isinstance(c, dict) and c.get("name")][:8],
            "probability": prob, "work_weeks": a.get("work_weeks"), "reasons": a.get("reasons") or {}}


def review(page, rows):
    r = page["properties"]
    ww_blank = r["Work Weeks"]["number"] is None
    idea = (f"Name: {get_text(r['Project'])}\nDescription: {get_text(r['Description'])}\nPain/Desire: {get_text(r['Pain/Desire'])}"
            + ("\nAlso estimate work_weeks." if ww_blank else f"\nWork weeks are already set ({r['Work Weeks']['number']}); return null."))
    return snap(ask_agent(RUBRIC.format(references=reference_lines(rows, exclude=page["id"]), idea=idea)))


def note(v):
    rs = v["reasons"]
    return "; ".join(f"{k}: {rs[k]}" for k in ("tam", "price", "competition", "probability") if rs.get(k))[:1900]


def write(page_id, v):
    props = {
        "TAM Customers": {"number": v["tam"]}, "TAM Sourced": {"checkbox": v["tam_sourced"]},
        "Price/Customer/yr ($)": {"number": v["price"]}, "Price Sourced": {"checkbox": v["price_sourced"]},
        "Competition": {"select": {"name": v["competition"]}}, "Probability": {"number": v["probability"]},
        "Review Note": {"rich_text": [{"text": {"content": note(v)}}]},
    }
    if v["tam_sourced"]:
        props.update({"TAM Population": {"number": v["population"]}, "TAM Share": {"number": v["share"]},
                      "TAM Source": {"url": v["tam_source"]},
                      "TAM Source Quote": {"rich_text": [{"text": {"content": str(v["tam_quote"])[:200]}}]}})
    if v["competitors"]:
        stored = json.dumps([{"name": c["name"], "evidence_url": c.get("url"), "why": c.get("why"), "funding_usd": c.get("funding_usd")}
                             for c in v["competitors"]], ensure_ascii=False)
        props["Competitors"] = {"rich_text": [{"text": {"content": stored[i:i + 2000]}} for i in range(0, len(stored), 2000)]}
    if v["work_weeks"]:
        props["Work Weeks"] = {"number": max(1, int(v["work_weeks"]))}
    notion_patch(f"pages/{page_id}", {"properties": props})

    remove_existing_validation_section(get_page_blocks(page_id))
    rs, bullet = v["reasons"], lambda t: {"bulleted_list_item": {"rich_text": [{"text": {"content": t[:1900]}}]}}
    price_text = (f"~${v['price_one_time']:,} one-time, counted as ${v['price']}/yr" if v["price_one_time"] else f"~${v['price']:,}/yr")
    blocks = [{"heading_2": {"rich_text": [{"text": {"content": f"Validation ({datetime.now():%b %Y}, agent review)"}}]}},
              bullet(f"👥 TAM: ~{v['tam']:,} customers — " + (f"{v['tam_quote']} ({v['tam_source']}) × {v['share']:g}. " if v["tam_sourced"] else "(assumed) ")
                     + rs.get("tam", "")),
              bullet(f"💵 Price: {price_text} — " + (f"\"{v['price_quote']}\" ({v['price_source']}). " if v["price_sourced"] else "(assumed) ")
                     + rs.get("price", "")),
              bullet(f"🏁 Competition: {v['competition']} — " + ", ".join(c["name"] for c in v["competitors"]) + ". " + rs.get("competition", "")),
              bullet(f"🎲 Probability: {v['probability']} — {rs.get('probability', '')}")]
    notion_patch(f"blocks/{page_id}/children", {"children": blocks})
    notion_patch(f"pages/{page_id}", {"properties": {"Validated": {"date": {"start": datetime.now(timezone.utc).isoformat(timespec="seconds")}}}})


def blind_test(n):
    """Re-score n hand-reviewed rows (their values and notes hidden from the agent) and count fields within one step."""
    rows = reviewed_rows()
    sample = random.Random(0).sample(rows, min(n, len(rows)))
    steps = lambda a, b: abs(math.log10(a) - math.log10(b)) if a and b else 9
    near = {"tam": 0, "price": 0, "competition": 0, "probability": 0}
    for p in sample:
        r = p["properties"]
        v = review(p, rows)
        hand = {"tam": r["TAM Customers"]["number"], "price": r["Price/Customer/yr ($)"]["number"],
                "competition": r["Competition"]["select"]["name"], "probability": r["Probability"]["number"]}
        near["tam"] += steps(v["tam"], hand["tam"]) <= 1
        near["price"] += steps(v["price"], hand["price"]) <= 1
        near["competition"] += abs(COMPETITION_LEVELS.index(v["competition"]) - COMPETITION_LEVELS.index(hand["competition"])) <= 1
        near["probability"] += abs(PROBABILITIES.index(v["probability"]) - PROBABILITIES.index(min(PROBABILITIES, key=lambda q: abs(q - hand["probability"])))) <= 1
        print(f"{get_text(r['Project'])[:30]:30} agent tam {v['tam']:>9,} ${v['price']:<6} {v['competition']:10} p{v['probability']:<6}"
              f" | hand {hand['tam']:>9,} ${hand['price']:<6} {hand['competition']:10} p{hand['probability']}", flush=True)
    print("within one step:", {k: f"{c}/{len(sample)}" for k, c in near.items()})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page_id", nargs="?")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--blind-test", type=int, metavar="N")
    args = ap.parse_args()
    if args.blind_test:
        return blind_test(args.blind_test)
    page = notion_get(f"pages/{args.page_id}")
    if page["properties"].get("Reviewed", {}).get("checkbox") and not args.dry_run:
        sys.exit("Reviewed by hand; uncheck Reviewed to let the agent rescore it")
    v = review(page, reviewed_rows())
    print(json.dumps(v, indent=2, ensure_ascii=False))
    if not args.dry_run:
        write(args.page_id, v)


if __name__ == "__main__":
    main()
