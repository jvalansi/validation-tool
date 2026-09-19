#!/usr/bin/env python3
"""
Project idea validation tool — multi-source signal aggregation.

Usage:
  python validation_tool.py hn --query QUERY [--limit N]
  python validation_tool.py trends --query QUERY [--timeframe "today 12-m"]
  python validation_tool.py producthunt --query QUERY [--limit N]
  python validation_tool.py incumbents --query QUERY [--limit N]
  python validation_tool.py report --query QUERY [--reddit-subreddits r/sub1,r/sub2]
"""

import argparse
import json
import os
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

def _fetch_trends(query, timeframe="today 12-m", retries=5, backoff=10):
    """Fetch Google Trends with exponential backoff on 429 / TooManyRequestsError."""
    import time
    from pytrends.request import TrendReq
    for attempt in range(retries):
        try:
            pytrends = TrendReq(hl="en-US", tz=360)
            pytrends.build_payload([query], timeframe=timeframe)
            return pytrends.interest_over_time()
        except Exception as e:
            msg = str(e)
            if attempt < retries - 1 and ("429" in msg or "Too Many" in msg or "timeout" in msg.lower()):
                wait = backoff * (2 ** attempt)
                sys.stderr.write(f"[trends] rate limited, retrying in {wait}s (attempt {attempt+1}/{retries})\n")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Google Trends: max retries exceeded")


def cmd_trends(args):
    try:
        from pytrends.request import TrendReq  # noqa — just checking install
    except ImportError:
        print(json.dumps({"error": "pytrends not installed. Run: pip install pytrends"}))
        sys.exit(1)

    interest = _fetch_trends(args.query, args.timeframe)
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
# Incumbents (businesses currently selling — Product Hunt only indexes launches)
# ---------------------------------------------------------------------------

FUNDED_INCUMBENT_USD = 10_000_000
CROWDED_OPERATORS = 5

_FUNDING_RE = re.compile(r'\$\s*(\d+(?:\.\d+)?)\s*(million|billion|m\b|b\b)', re.IGNORECASE)
_FUNDING_CONTEXT = ("raise", "raised", "raises", "funding", "series ", "seed round", "venture", "backed")

# Hosts that aggregate or discuss vendors rather than being vendors themselves.
_DIRECTORY_HOSTS = (
    "wikipedia.org", "reddit.com", "youtube.com", "producthunt.com", "linkedin.com",
    "facebook.com", "twitter.com", "x.com", "quora.com", "medium.com", "g2.com",
    "capterra.com", "crunchbase.com", "pitchbook.com", "glassdoor.com", "indeed.com",
    "news.ycombinator.com", "substack.com",
)


def _parse_funding(text):
    """Largest USD funding amount mentioned in text, or None.

    Requires funding language nearby so '$400 million saved for customers' is
    ignored while '$50 million Series B' is not.
    """
    if not text:
        return None
    if not any(k in text.lower() for k in _FUNDING_CONTEXT):
        return None
    best = None
    for m in _FUNDING_RE.finditer(text):
        unit = m.group(2).lower()
        usd = float(m.group(1)) * (1_000_000_000 if unit.startswith("b") else 1_000_000)
        if best is None or usd > best:
            best = usd
    return best


def _host(url):
    try:
        return urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return ""


def _incumbent_search(query, limit=8):
    """Find who is already selling this, and how much they have raised.

    Product Hunt indexes launches, so a company that launched years ago and now
    dominates the market never shows up there. These probes target pricing pages
    and funding news instead.
    """
    from ddgs import DDGS

    operators, funding = {}, []
    probes = [
        (f"{query} pricing", "pricing"),
        (f"{query} service cost fee", "pricing"),
        (f"{query} startup raised funding round", "funding"),
    ]
    for probe, kind in probes:
        try:
            hits = list(DDGS().text(probe, max_results=limit))
        except Exception:
            continue
        for r in hits:
            url = r.get("href", "")
            title = (r.get("title") or "").strip()
            snippet = (r.get("body") or "").strip()
            host = _host(url)
            if not host or any(host == d or host.endswith("." + d) for d in _DIRECTORY_HOSTS):
                continue
            amount = _parse_funding(f"{title} {snippet}")
            if amount:
                funding.append({"amount_usd": amount, "headline": title[:120], "url": url})
            if kind == "pricing" and host not in operators:
                operators[host] = {"name": title[:80], "host": host, "url": url, "snippet": snippet[:200]}

    funding.sort(key=lambda f: f["amount_usd"], reverse=True)
    return {
        "operators_found": len(operators),
        "operators": list(operators.values())[:6],
        "funding_mentions": funding[:3],
        "max_funding_usd": funding[0]["amount_usd"] if funding else None,
    }


def _assess_competition(incumbents, product_hunt):
    """Turn incumbent data into signals. Absence of competitors is NOT a positive.

    An empty result means demand is unproven or the query was too abstract — the
    old 'no PH solutions yet (gap)' rule scored that as upside and mis-passed
    markets whose incumbents simply predate Product Hunt.
    """
    positives, negatives = [], []
    ops = incumbents.get("operators_found", 0)
    max_funding = incumbents.get("max_funding_usd")

    if max_funding and max_funding >= FUNDED_INCUMBENT_USD:
        negatives.append(f"funded incumbent (${round(max_funding / 1_000_000)}M raised)")
        level = "funded_incumbent"
    elif ops >= CROWDED_OPERATORS:
        negatives.append(f"crowded: {ops} vendors already selling")
        level = "crowded"
    elif ops >= 1:
        positives.append(f"{ops} small vendor(s) selling — demand proven, room to differentiate")
        level = "contested"
    else:
        negatives.append("no vendors found selling this — demand unproven, or query too abstract")
        level = "none_found"

    ph_count = product_hunt.get("existing_products", 0)
    if ph_count >= CROWDED_OPERATORS:
        negatives.append(f"{ph_count} Product Hunt launches in this space")

    return {"positive": positives, "negative": negatives, "level": level}


def cmd_incumbents(args):
    print(json.dumps(_incumbent_search(args.query, limit=args.limit), indent=2, ensure_ascii=False))


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

    search_query = args.pain_query if (getattr(args, "assume_tech_exists", False) and getattr(args, "pain_query", None)) else args.query
    report = {"query": args.query, "search_query": search_query, "sources": {}}

    # HN
    try:
        params = urllib.parse.urlencode({"query": search_query, "tags": "story", "hitsPerPage": 10})
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

    # Google Trends (explicit trends_query takes priority, then search_query, then pain_query fallback)
    pain_query = getattr(args, "pain_query", None)
    explicit_trends_query = getattr(args, "trends_query", None)
    trends_queries = [explicit_trends_query or search_query]
    if pain_query and pain_query != trends_queries[0]:
        trends_queries.append(pain_query)
    trends_result = None
    for tq in trends_queries:
        try:
            interest = _fetch_trends(tq)
            if not interest.empty:
                col = tq if tq in interest.columns else interest.columns[0]
                values = interest[col].tolist()
                recent = values[-4:]
                avg = round(sum(values) / len(values), 1)
                trend_dir = "up" if recent[-1] > recent[0] else "down" if recent[-1] < recent[0] else "flat"
                trends_result = {
                    "average_interest": avg,
                    "trend_direction": trend_dir,
                    "signal": "strong" if avg > 50 else "moderate" if avg > 20 else "weak",
                    "query_used": tq,
                }
                break
        except Exception as e:
            trends_result = {"error": str(e)}
    report["sources"]["google_trends"] = trends_result or {"signal": "no data"}

    # Reddit (via DuckDuckGo site:reddit.com — no auth needed)
    try:
        reddit_posts = _reddit_search(search_query, args.reddit_subreddits, limit=10)
        report["sources"]["reddit"] = {
            "total_results": len(reddit_posts),
            "top_posts": [{"title": p["title"], "url": p["url"], "snippet": p["snippet"][:150]} for p in reddit_posts[:3]],
        }
    except Exception as e:
        report["sources"]["reddit"] = {"error": str(e)}

    # Product Hunt (via DDG)
    try:
        ph_results = _ph_search(search_query, limit=5)
        report["sources"]["product_hunt"] = {
            "existing_products": len(ph_results),
            "top_products": [{"name": r["title"], "url": r["url"], "snippet": r["snippet"][:100]} for r in ph_results[:3]],
        }
    except Exception as e:
        report["sources"]["product_hunt"] = {"error": str(e)}

    # Incumbents (operating businesses + funding — catches what Product Hunt misses)
    try:
        report["sources"]["incumbents"] = _incumbent_search(search_query)
    except Exception as e:
        report["sources"]["incumbents"] = {"error": str(e)}

    # Revenue estimate
    all_snippets = []
    for ph_item in report["sources"].get("product_hunt", {}).get("top_products", []):
        all_snippets.append(ph_item.get("snippet", ""))
    for hn_item in report["sources"].get("hacker_news", {}).get("top_posts", []):
        all_snippets.append(hn_item.get("title", ""))
    for rd_item in report["sources"].get("reddit", {}).get("top_posts", []):
        all_snippets.append(rd_item.get("snippet", ""))
    for op in report["sources"].get("incumbents", {}).get("operators", []):
        all_snippets.append(op.get("snippet", ""))

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
    comp = _assess_competition(report["sources"].get("incumbents", {}), ph)
    signals.extend(comp["positive"])

    if comp["level"] == "funded_incumbent":
        verdict = "crowded — a funded incumbent already serves this market"
    elif comp["level"] == "crowded":
        verdict = "crowded — multiple vendors already selling"
    elif len(signals) >= 2:
        verdict = "validate further"
    else:
        verdict = "weak signal — reconsider or reframe"

    report["summary"] = {
        "positive_signals": signals,
        "negative_signals": comp["negative"],
        "signal_count": len(signals),
        "competition": comp["level"],
        "verdict": verdict,
    }

    # Claude synthesis
    claude_analysis = _claude_review(args.query, report, assume_tech_exists=getattr(args, "assume_tech_exists", False))
    if claude_analysis:
        # OOM-round numeric fields so callers get canonical values
        for field in ("tam_customers", "price_per_customer_annual", "value"):
            v = claude_analysis.get(field)
            if isinstance(v, (int, float)) and v > 0:
                import math as _math
                claude_analysis[field] = int(10 ** round(_math.log10(v)))
        # Map probability to OOM scale: 0.01 moonshot / 0.10 standard / 1.0 straightforward
        prob = claude_analysis.get("suggested_probability")
        if prob is not None:
            claude_analysis["suggested_probability"] = 1.0 if prob >= 0.5 else 0.1 if prob >= 0.05 else 0.01
        report["claude_analysis"] = claude_analysis

    print(json.dumps(report, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Claude revenue/value synthesis
# ---------------------------------------------------------------------------

def _claude_review(query, report, assume_tech_exists=False):
    """Call Claude via CLI to synthesize the report data into a revenue/value estimate."""
    import subprocess
    import shutil

    claude_path = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    if not os.path.exists(claude_path):
        return None

    tech_context = (
        "IMPORTANT ASSUMPTION: Treat the technology as fully working and available. "
        "Do NOT factor in technical feasibility or R&D risk — those are captured separately in the probability of success. "
        "Focus purely on market demand: if this product existed today and worked perfectly, would people pay for it and how much?"
        if assume_tech_exists else ""
    )

    prompt = f"""You are a startup analyst. Given the following market research data for the idea "{query}", provide a concise revenue and value assessment.

{tech_context}

Research data:
{json.dumps(report.get("sources", {}), indent=2)}

Revenue signals extracted:
{json.dumps(report.get("revenue_estimate", {}), indent=2)}

All numeric outputs must be rounded to the nearest power of 10 (e.g. 100, 1000, 10000, 100000, 1000000). Do not use precise figures — order-of-magnitude accuracy is the goal.

Provide your assessment as JSON with these fields:
- "tam_assessment": one sentence on market size (mention specific evidence from the data)
- "tam_customers": estimated number of potential customers, rounded to nearest power of 10
- "price_per_customer_annual": estimated annual revenue per customer in USD, rounded to nearest power of 10 (e.g. 100 for ~$8-12/mo, 1000 for ~$80-120/mo)
- "pricing_assessment": one sentence on pricing strategy and willingness to pay (e.g. "B2B SaaS at ~$100/yr is realistic given competitor pricing")
- "key_risks": list of 2-3 main risks to revenue (exclude technical feasibility risk)
- "key_opportunities": list of 2-3 strongest signals supporting the idea
- "value": total addressable annual revenue in USD, rounded to nearest power of 10 — this is the FULL market potential (tam_customers × price_per_customer_annual), with NO adjustment for penetration or probability. Do not discount for competition or execution risk here.
- "value_reasoning": one sentence explaining the value estimate (reference tam_customers × price_per_customer_annual)
- "suggested_probability": expected fraction of the total value that will actually be captured, using exactly one of these three values:
    0.01 — moonshot: paradigm shift required, or tiny realistic penetration (e.g. <1% of a niche market)
    0.10 — regular challenge: real demand and proven tech, but significant competition or execution risk (realistic penetration ~5-15%)
    0.99 — low-hanging fruit: clear unmet demand, proven solution, little competition (high penetration likely)
  This encodes both probability of success AND realistic market penetration. Choose the closest tier.
- "probability_reasoning": one sentence explaining the probability choice, including the expected penetration rate

Return only valid JSON, no markdown."""

    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        result = subprocess.run(
            [claude_path, "-p", prompt, "--output-format", "json", "--dangerously-skip-permissions"],
            capture_output=True, text=True, timeout=120,
            env=env, cwd="/home/ubuntu"
        )
        if result.returncode == 0 and result.stdout.strip():
            outer = json.loads(result.stdout)
            text = outer.get("result", "").strip()
            if text.startswith("```"):
                text = "\n".join(text.split("\n")[1:])
                text = text.rsplit("```", 1)[0].strip()
            return json.loads(text)
    except Exception as e:
        return {"error": str(e)}

    return None


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

    p_inc = subparsers.add_parser("incumbents", help="Find businesses already selling this + their funding")
    p_inc.add_argument("--query", required=True)
    p_inc.add_argument("--limit", type=int, default=8)

    p_reddit = subparsers.add_parser("reddit", help="Search Reddit (no auth needed)")
    p_reddit.add_argument("--query", required=True)
    p_reddit.add_argument("--subreddits", help="Comma-separated subreddits (optional, default: all)")
    p_reddit.add_argument("--limit", type=int, default=10)

    p_report = subparsers.add_parser("report", help="Full multi-source validation report")
    p_report.add_argument("--query", required=True)
    p_report.add_argument("--reddit-subreddits", help="Comma-separated subreddits to search (optional)")
    p_report.add_argument("--assume-tech-exists", action="store_true",
                          help="Assume technology works — assess market demand only, not technical feasibility")
    p_report.add_argument("--pain-query", help="Pain/desire search query to use instead of product query (used with --assume-tech-exists)")
    p_report.add_argument("--trends-query", help="Specific short query to use for Google Trends (overrides default query)")

    args = parser.parse_args()

    if args.command == "hn":
        cmd_hn(args)
    elif args.command == "trends":
        cmd_trends(args)
    elif args.command == "producthunt":
        cmd_producthunt(args)
    elif args.command == "incumbents":
        cmd_incumbents(args)
    elif args.command == "reddit":
        cmd_reddit(args)
    elif args.command == "report":
        cmd_report(args)


if __name__ == "__main__":
    main()
