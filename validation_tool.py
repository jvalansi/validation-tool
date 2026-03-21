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
# Product Hunt (public API v2 — no auth needed for basic search)
# ---------------------------------------------------------------------------

PH_API_URL = "https://api.producthunt.com/v2/api/graphql"


def _ph_fetch_posts(ph_token, first=50):
    """Fetch recent top posts from PH (API v2 has no free-text search)."""
    gql = """
    query($first: Int!) {
      posts(order: VOTES, first: $first) {
        nodes {
          id name tagline votesCount commentsCount website url createdAt
          topics { nodes { name } }
        }
      }
    }
    """
    payload = json.dumps({"query": gql, "variables": {"first": first}}).encode()
    req = urllib.request.Request(
        PH_API_URL, data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {ph_token}"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    return data.get("data", {}).get("posts", {}).get("nodes", [])


def cmd_producthunt(args):
    ph_token = _get_ph_token()
    if not ph_token:
        print(json.dumps({"error": "PRODUCTHUNT_TOKEN not set."}))
        sys.exit(1)

    keywords = [w.lower() for w in args.query.split()]
    nodes = _ph_fetch_posts(ph_token, first=200)

    results = []
    for n in nodes:
        text = (n["name"] + " " + n["tagline"]).lower()
        topic_names = [t["name"].lower() for t in n.get("topics", {}).get("nodes", [])]
        combined = text + " " + " ".join(topic_names)
        if all(kw in combined for kw in keywords):
            results.append({
                "id": n["id"],
                "name": n["name"],
                "tagline": n["tagline"],
                "votes": n["votesCount"],
                "comments": n["commentsCount"],
                "url": n["url"],
                "website": n.get("website", ""),
                "created_at": n["createdAt"][:10],
                "topics": [t["name"] for t in n.get("topics", {}).get("nodes", [])],
            })
            if len(results) >= args.limit:
                break

    print(json.dumps(results, indent=2, ensure_ascii=False))


def _get_ph_token():
    import os
    return os.environ.get("PRODUCTHUNT_TOKEN")


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

    # Reddit
    try:
        reddit_tool = os.path.join(os.path.dirname(__file__), "..", "reddit-tool", "reddit_tool.py")
        python = sys.executable
        cmd = [python, reddit_tool, "search", "--query", args.query, "--limit", "5"]
        if args.reddit_subreddits:
            cmd += ["--subreddits", args.reddit_subreddits]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            posts = json.loads(result.stdout)
            report["sources"]["reddit"] = {
                "total_results": len(posts),
                "top_posts": [
                    {"title": p["title"], "score": p["score"], "comments": p["num_comments"], "url": p["url"]}
                    for p in sorted(posts, key=lambda x: x["score"], reverse=True)[:3]
                ],
            }
        else:
            report["sources"]["reddit"] = {"error": result.stderr.strip()}
    except Exception as e:
        report["sources"]["reddit"] = {"error": str(e)}

    # Product Hunt
    ph_token = _get_ph_token()
    if ph_token:
        try:
            keywords = [w.lower() for w in args.query.split()]
            all_nodes = _ph_fetch_posts(ph_token, first=200)
            nodes = []
            for n in all_nodes:
                text = (n["name"] + " " + n["tagline"]).lower()
                topic_names = [t["name"].lower() for t in n.get("topics", {}).get("nodes", [])]
                combined = text + " " + " ".join(topic_names)
                if all(kw in combined for kw in keywords):
                    nodes.append(n)
                if len(nodes) >= 5:
                    break
            report["sources"]["product_hunt"] = {
                "existing_products": len(nodes),
                "top_products": [{"name": n["name"], "tagline": n["tagline"], "votes": n["votesCount"]} for n in nodes[:3]],
            }
        except Exception as e:
            report["sources"]["product_hunt"] = {"error": str(e)}
    else:
        report["sources"]["product_hunt"] = {"skipped": "PRODUCTHUNT_TOKEN not set"}

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
    if rd.get("total_results", 0) > 10:
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
    elif args.command == "report":
        cmd_report(args)


if __name__ == "__main__":
    main()
