#!/usr/bin/env python3
"""
Project idea validation tool — multi-source signal aggregation.

Usage:
  python validation_tool.py hn --query QUERY [--limit N]
  python validation_tool.py trends --query QUERY [--timeframe "today 12-m"]
  python validation_tool.py producthunt --query QUERY [--limit N]
  python validation_tool.py report --query QUERY [--reddit-subreddits r/sub1,r/sub2]
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Hacker News (Algolia API — no auth needed)
# ---------------------------------------------------------------------------

HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"


def cmd_hn(args):
    params = urllib.parse.urlencode({
        "query": args.query,
        "tags": "story",
        "hitsPerPage": args.limit,
    })
    url = f"{HN_SEARCH_URL}?{params}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read())

    results = []
    for hit in data.get("hits", []):
        results.append({
            "id": hit.get("objectID"),
            "title": hit.get("title"),
            "points": hit.get("points", 0),
            "num_comments": hit.get("num_comments", 0),
            "url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "story_url": hit.get("url", ""),
            "created_at": hit.get("created_at", ""),
        })

    results.sort(key=lambda x: x["points"], reverse=True)
    print(json.dumps(results, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Google Trends (pytrends)
# ---------------------------------------------------------------------------

def cmd_trends(args):
    try:
        from pytrends.request import TrendReq
    except ImportError:
        print(json.dumps({"error": "pytrends not installed. Run: pip install pytrends"}))
        sys.exit(1)

    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload([args.query], timeframe=args.timeframe)

    interest = pytrends.interest_over_time()
    if interest.empty:
        print(json.dumps({"query": args.query, "trend": [], "average": 0, "note": "No data returned"}))
        return

    col = args.query if args.query in interest.columns else interest.columns[0]
    values = interest[col].tolist()
    dates = [str(d.date()) for d in interest.index]

    avg = round(sum(values) / len(values), 1) if values else 0
    recent = values[-4:] if len(values) >= 4 else values
    trend_direction = "up" if recent[-1] > recent[0] else "down" if recent[-1] < recent[0] else "flat"

    print(json.dumps({
        "query": args.query,
        "timeframe": args.timeframe,
        "average_interest": avg,
        "trend_direction": trend_direction,
        "recent_values": list(zip(dates[-12:], values[-12:])),
    }, indent=2))


# ---------------------------------------------------------------------------
# Reddit (unofficial JSON API — no auth needed)
# ---------------------------------------------------------------------------

def _reddit_search(query, subreddits=None, limit=10):
    from ddgs import DDGS
    if subreddits:
        subs = [s.strip() for s in subreddits.split(",")]
        sub_filter = " OR ".join("r/" + s.lstrip("r/") for s in subs)
        ddg_query = f"site:reddit.com ({sub_filter}) {query}"
    else:
        ddg_query = f"site:reddit.com {query}"

    results = []
    for r in DDGS().text(ddg_query, max_results=limit):
        results.append({
            "title": r["title"],
            "url": r["href"],
            "snippet": r["body"],
        })
    return results


def cmd_reddit(args):
    results = _reddit_search(args.query, args.subreddits, limit=args.limit)
    print(json.dumps(results, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Product Hunt (via DuckDuckGo site:producthunt.com — no auth needed)
# ---------------------------------------------------------------------------

def _ph_search(query, limit=10):
    from ddgs import DDGS
    ddg_query = f"site:producthunt.com/products {query}"
    results = []
    for r in DDGS().text(ddg_query, max_results=limit):
        # Filter out non-product pages (alternatives, makers, profiles)
        url = r["href"]
        if any(x in url for x in ["/alternatives", "/makers", "/@", "/discussion"]):
            continue
        results.append({
            "title": r["title"].replace(" | Product Hunt", "").strip(),
            "url": url,
            "snippet": r["body"],
        })
    return results


def cmd_producthunt(args):
    results = _ph_search(args.query, limit=args.limit)
    print(json.dumps(results, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Revenue signal helpers
# ---------------------------------------------------------------------------

_PRICE_RE = re.compile(
    r'\$\s*(\d+(?:\.\d+)?)\s*(?:per\s+)?(?:/\s*)?(mo(?:nth)?|yr|year|user|seat|month)?',
    re.IGNORECASE
)

def _extract_prices(texts):
    """Extract price mentions from a list of strings. Returns list of dicts."""
    found = []
    for text in texts:
        for m in _PRICE_RE.finditer(text or ""):
            amount = float(m.group(1))
            period = (m.group(2) or "").lower()
            if period in ("yr", "year"):
                amount_mo = round(amount / 12, 2)
            else:
                amount_mo = amount
            if 1 <= amount_mo <= 10000:  # filter noise
                found.append({"raw": m.group(0).strip(), "monthly_equiv": amount_mo})
    # deduplicate
    seen = set()
    unique = []
    for p in found:
        key = p["raw"]
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def _tam_tier(trends_avg):
    if trends_avg >= 50:
        return "mass"
    if trends_avg >= 20:
        return "mid"
    return "niche"


def _mrr_range(tam_tier, prices):
    monthly_prices = [p["monthly_equiv"] for p in prices] if prices else []
    price_anchor = sorted(monthly_prices)[len(monthly_prices) // 2] if monthly_prices else None

    ranges = {
        "mass":  {"conservative": (500, 5000),  "optimistic": (10000, 50000)},
        "mid":   {"conservative": (100, 1000),  "optimistic": (2000, 10000)},
        "niche": {"conservative": (50,  500),   "optimistic": (500,  3000)},
    }
    r = ranges[tam_tier]

    # scale up if competitors charge premium prices
    if price_anchor and price_anchor > 50:
        r = {k: (v[0] * 2, v[1] * 2) for k, v in r.items()}

    return {
        "conservative_mrr": f"${r['conservative'][0]}–${r['conservative'][1]}",
        "optimistic_mrr":   f"${r['optimistic'][0]}–${r['optimistic'][1]}",
        "price_anchor_used": f"${price_anchor}/mo" if price_anchor else "no prices found — used defaults",
    }


# ---------------------------------------------------------------------------
# Full validation report
# ---------------------------------------------------------------------------

def cmd_report(args):
    import subprocess
    import os

    report = {"query": args.query, "sources": {}}

    # HN
    try:
        params = urllib.parse.urlencode({"query": args.query, "tags": "story", "hitsPerPage": 10})
        with urllib.request.urlopen(f"{HN_SEARCH_URL}?{params}", timeout=10) as resp:
            data = json.loads(resp.read())
        hits = data.get("hits", [])
        report["sources"]["hacker_news"] = {
            "total_results": data.get("nbHits", 0),
            "top_posts": [
                {"title": h["title"], "points": h.get("points", 0), "url": f"https://news.ycombinator.com/item?id={h['objectID']}"}
                for h in sorted(hits, key=lambda x: x.get("points", 0), reverse=True)[:3]
            ],
        }
    except Exception as e:
        report["sources"]["hacker_news"] = {"error": str(e)}

    # Google Trends
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload([args.query], timeframe="today 12-m")
        interest = pytrends.interest_over_time()
        if not interest.empty:
            col = args.query if args.query in interest.columns else interest.columns[0]
            values = interest[col].tolist()
            recent = values[-4:]
            avg = round(sum(values) / len(values), 1)
            trend_dir = "up" if recent[-1] > recent[0] else "down" if recent[-1] < recent[0] else "flat"
            report["sources"]["google_trends"] = {
                "average_interest": avg,
                "trend_direction": trend_dir,
                "signal": "strong" if avg > 50 else "moderate" if avg > 20 else "weak",
            }
        else:
            report["sources"]["google_trends"] = {"signal": "no data"}
    except Exception as e:
        report["sources"]["google_trends"] = {"error": str(e)}

    # Reddit (via DuckDuckGo site:reddit.com — no auth needed)
    try:
        reddit_posts = _reddit_search(args.query, args.reddit_subreddits, limit=10)
        report["sources"]["reddit"] = {
            "total_results": len(reddit_posts),
            "top_posts": [{"title": p["title"], "url": p["url"], "snippet": p["snippet"][:150]} for p in reddit_posts[:3]],
        }
    except Exception as e:
        report["sources"]["reddit"] = {"error": str(e)}

    # Product Hunt (via DDG)
    try:
        ph_results = _ph_search(args.query, limit=5)
        report["sources"]["product_hunt"] = {
            "existing_products": len(ph_results),
            "top_products": [{"name": r["title"], "url": r["url"], "snippet": r["snippet"][:100]} for r in ph_results[:3]],
        }
    except Exception as e:
        report["sources"]["product_hunt"] = {"error": str(e)}

    # Revenue estimate
    all_snippets = []
    for ph_item in report["sources"].get("product_hunt", {}).get("top_products", []):
        all_snippets.append(ph_item.get("snippet", ""))
    for hn_item in report["sources"].get("hacker_news", {}).get("top_posts", []):
        all_snippets.append(hn_item.get("title", ""))
    for rd_item in report["sources"].get("reddit", {}).get("top_posts", []):
        all_snippets.append(rd_item.get("snippet", ""))

    competitor_prices = _extract_prices(all_snippets)
    trends_avg = report["sources"].get("google_trends", {}).get("average_interest", 0)
    tam = _tam_tier(trends_avg)
    mrr = _mrr_range(tam, competitor_prices)

    report["revenue_estimate"] = {
        "tam_tier": tam,
        "competitor_prices_found": competitor_prices,
        **mrr,
        "note": (
            "Rough estimate based on TAM tier (Google Trends) and competitor pricing extracted from snippets. "
            "Assumes 2–5% free→paid conversion and ~100–500 monthly visitors at conservative end."
        ),
    }

    # Summary signal
    signals = []
    hn = report["sources"].get("hacker_news", {})
    if hn.get("total_results", 0) > 20:
        signals.append("high HN interest")
    gt = report["sources"].get("google_trends", {})
    if gt.get("trend_direction") == "up":
        signals.append("growing search trend")
    if gt.get("signal") == "strong":
        signals.append("strong search volume")
    rd = report["sources"].get("reddit", {})
    if rd.get("total_results", 0) > 5:
        signals.append("active Reddit discussion")
    ph = report["sources"].get("product_hunt", {})
    if 0 < ph.get("existing_products", 0) < 5:
        signals.append("few existing PH solutions (gap)")
    elif ph.get("existing_products", 0) == 0:
        signals.append("no PH solutions yet (untapped or too niche)")

    report["summary"] = {
        "positive_signals": signals,
        "signal_count": len(signals),
        "verdict": "validate further" if len(signals) >= 2 else "weak signal — reconsider or reframe",
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Project idea validation tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_hn = subparsers.add_parser("hn", help="Search Hacker News for pain points")
    p_hn.add_argument("--query", required=True)
    p_hn.add_argument("--limit", type=int, default=20)

    p_trends = subparsers.add_parser("trends", help="Check Google Trends interest")
    p_trends.add_argument("--query", required=True)
    p_trends.add_argument("--timeframe", default="today 12-m", help="e.g. 'today 12-m', 'today 5-y'")

    p_ph = subparsers.add_parser("producthunt", help="Search Product Hunt for existing products")
    p_ph.add_argument("--query", required=True)
    p_ph.add_argument("--limit", type=int, default=10)

    p_reddit = subparsers.add_parser("reddit", help="Search Reddit (no auth needed)")
    p_reddit.add_argument("--query", required=True)
    p_reddit.add_argument("--subreddits", help="Comma-separated subreddits (optional, default: all)")
    p_reddit.add_argument("--limit", type=int, default=10)

    p_report = subparsers.add_parser("report", help="Full multi-source validation report")
    p_report.add_argument("--query", required=True)
    p_report.add_argument("--reddit-subreddits", help="Comma-separated subreddits to search (optional)")

    args = parser.parse_args()

    if args.command == "hn":
        cmd_hn(args)
    elif args.command == "trends":
        cmd_trends(args)
    elif args.command == "producthunt":
        cmd_producthunt(args)
    elif args.command == "reddit":
        cmd_reddit(args)
    elif args.command == "report":
        cmd_report(args)


if __name__ == "__main__":
    main()
