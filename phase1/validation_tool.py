#!/usr/bin/env python3
"""
Project idea validation tool — multi-source signal aggregation.

Usage:
  python validation_tool.py hn --query QUERY [--limit N]
  python validation_tool.py trends --query QUERY [--timeframe "today 12-m"]
  python validation_tool.py producthunt --query QUERY [--limit N]
  python validation_tool.py incumbents --query QUERY [--limit N]
  python validation_tool.py regulatory --query QUERY
  python validation_tool.py serp --query QUERY [--limit N]
  python validation_tool.py report --query QUERY [--reddit-subreddits r/sub1,r/sub2]
"""

import argparse
import math
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Web search
# ---------------------------------------------------------------------------

BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
EXIT_SEARCH_REFUSED = 3  # report --require-brave exit code: Brave refused, nothing written, resume later
_brave_refused = []  # HTTP codes; with --require-brave the report is discarded if any search was refused


def _web_search(query, max_results=10):
    """[{title, href, body}] from the Brave Search API when BRAVE_API_KEY is set, else ddgs.
    ddgs reads results pages of a randomly shuffled engine per call (ddgs/ddgs.py), most of which
    block this server, so the same query returns different results run to run."""
    from ddgs import DDGS
    key = os.environ.get("BRAVE_API_KEY")
    if not key:
        return list(DDGS().text(query, max_results=max_results))
    params = urllib.parse.urlencode({"q": query, "count": min(max_results, 20)})
    req = urllib.request.Request(f"{BRAVE_SEARCH_URL}?{params}", headers={
        "X-Subscription-Token": key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            results = json.loads(resp.read()).get("web", {}).get("results", [])
    except urllib.error.HTTPError as e:  # 402 = prepaid credit used up, 429 = rate limit
        _brave_refused.append(e.code)
        sys.stderr.write(f"[search] Brave HTTP {e.code}, falling back to ddgs: {e.read()[:200]!r}\n")
        return list(DDGS().text(query, max_results=max_results))
    strip = lambda t: re.sub(r"<[^>]+>", "", t or "")  # Brave bolds matches with <strong>
    return [{"title": strip(r.get("title")), "href": r.get("url", ""), "body": strip(r.get("description"))}
            for r in results][:max_results]


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
    if subreddits:
        subs = [s.strip() for s in subreddits.split(",")]
        sub_filter = " OR ".join("r/" + s.lstrip("r/") for s in subs)
        ddg_query = f"site:reddit.com ({sub_filter}) {query}"
    else:
        ddg_query = f"site:reddit.com {query}"

    results = []
    for r in _web_search(ddg_query, max_results=limit):
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
    ddg_query = f"site:producthunt.com/products {query}"
    results = []
    for r in _web_search(ddg_query, max_results=limit):
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

DOMINANT_FUNDING_USD = 100_000_000   # a category owner — outspends you on every channel
FUNDED_FUNDING_USD = 10_000_000      # funded, but not untouchable
CROWDED_OPERATORS = 8                # operator counts include review-site noise; keep this loose
CROWDED_PH_LAUNCHES = 5              # launches are cheap to count, so a tighter bar

_FUNDING_RE = re.compile(r'\$\s*(\d+(?:\.\d+)?)\s*(million|billion|m\b|b\b)', re.IGNORECASE)
_FUNDING_CONTEXT = ("raise", "raised", "raises", "funding", "series ", "seed round", "venture", "backed")

# Hosts that aggregate or discuss vendors rather than being vendors themselves.
_DIRECTORY_HOSTS = (
    "wikipedia.org", "reddit.com", "youtube.com", "producthunt.com", "linkedin.com",
    "facebook.com", "twitter.com", "x.com", "quora.com", "medium.com", "g2.com",
    "capterra.com", "crunchbase.com", "pitchbook.com", "glassdoor.com", "indeed.com",
    "news.ycombinator.com", "substack.com",
)

# Papers, code hosts and docs rank for pricing probes in academic niches but sell
# nothing — counting them turned every neuroscience-tooling idea "crowded", and
# "$1"/"$8" scraped from a Frontiers paper became the price anchor.
_NON_VENDOR_HOSTS = (
    "github.com", "github.io", "gitlab.com", "readthedocs.io", "arxiv.org", "biorxiv.org",
    "medrxiv.org", "nih.gov", "elifesciences.org", "frontiersin.org", "springer.com",
    "sciencedirect.com", "nature.com", "cell.com", "wiley.com", "plos.org", "mdpi.com",
    "ieee.org", "researchgate.net", "sagepub.com", "tandfonline.com", "oup.com",
    "biomedcentral.com", "iop.org", "acm.org", "semanticscholar.org", "zenodo.org",
    "pubmed.gov", "jneurosci.org", "physiology.org", "hal.science",
)
_NON_VENDOR_SUFFIXES = (".edu", ".gov", ".mil")
_NON_VENDOR_LABELS = ("ac", "edu")  # ucl.ac.uk, unimelb.edu.au


def _is_non_vendor(host):
    """True for hosts that cannot be a competitor selling the product."""
    if any(host == d or host.endswith("." + d) for d in _DIRECTORY_HOSTS + _NON_VENDOR_HOSTS):
        return True
    if host.endswith(_NON_VENDOR_SUFFIXES):
        return True
    parts = host.split(".")
    return len(parts) >= 3 and parts[-2] in _NON_VENDOR_LABELS


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

    import time
    tokens = _query_tokens(query)
    operators, funding = {}, []
    failed = 0
    probes = [
        (f"{query} pricing", "pricing"),
        (f"{query} service cost fee", "pricing"),
        (f"{query} startup raised funding round", "funding"),
    ]
    for i, (probe, kind) in enumerate(probes):
        if i:
            time.sleep(2)  # see _regulatory_search: a rate-limited 0 must not read as "no competitors"
        try:
            hits = _web_search(probe, max_results=limit)
        except Exception:
            time.sleep(10)  # usually a rate limit; one retry before counting it as failed
            try:
                hits = _web_search(probe, max_results=limit)
            except Exception:
                failed += 1
                continue
        for r in hits:
            url = r.get("href", "")
            title = (r.get("title") or "").strip()
            snippet = (r.get("body") or "").strip()
            host = _host(url)
            if not host or _is_non_vendor(host):
                continue
            amount = _parse_funding(f"{title} {snippet}")
            if amount and not [t for t in tokens if t in f"{title} {snippet}".lower()]:
                amount = None  # a raise with no query overlap is some other market's news
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
        "probes_failed": failed,
        "search_failed": failed == len(probes),
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

    # Any failed probe, not just all of them: a dropped funding probe reads as "no funded competitor".
    if incumbents.get("search_failed") or incumbents.get("probes_failed") or incumbents.get("error"):
        negatives.append("incumbent search unavailable — competition unknown, not absent")
        return {"positive": positives, "negative": negatives, "level": "unknown"}

    raised = f"${round(max_funding / 1_000_000)}M raised" if max_funding else ""

    if max_funding and max_funding >= DOMINANT_FUNDING_USD:
        negatives.append(f"category owner in the market ({raised}) — outspends you on every channel")
        level = "dominant"
    elif max_funding and max_funding >= FUNDED_FUNDING_USD and ops >= CROWDED_OPERATORS:
        # Funding AND a full field: the money is not the only thing in the way.
        negatives.append(f"funded competitor ({raised}) among {ops} vendors already selling")
        level = "crowded"
    elif max_funding and max_funding >= FUNDED_FUNDING_USD:
        negatives.append(f"funded competitor ({raised}) — beatable, but not on spend")
        positives.append("funding in the space confirms investors believe the demand")
        level = "funded"
    elif ops >= CROWDED_OPERATORS:
        negatives.append(f"crowded: {ops} vendors already selling")
        level = "crowded"
    elif ops >= 2:
        positives.append(f"{ops} small vendors selling, none funded — demand proven, room to differentiate")
        level = "contested"
    elif ops == 1:
        positives.append("1 vendor selling — demand proven, market barely served")
        level = "open"
    else:
        negatives.append("no vendors found selling this — demand unproven, or query too abstract")
        level = "none_found"

    ph_count = product_hunt.get("existing_products", 0)
    if ph_count >= CROWDED_PH_LAUNCHES:
        negatives.append(f"{ph_count} Product Hunt launches in this space")

    return {"positive": positives, "negative": negatives, "level": level}


def cmd_incumbents(args):
    print(json.dumps(_incumbent_search(args.query, limit=args.limit), indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Regulatory standing (are you allowed to sell it?)
# ---------------------------------------------------------------------------

_RESTRICTION_TERMS = (
    "license required", "must be licensed", "licensed attorney", "unauthorized practice",
    "only an attorney", "registration required", "bar admission", "regulated by",
    "licensed agent", "not permitted to represent", "not qualified to practice",
    "practice of law", "licensed professional", "statutory exemption",
    "state law requires", "certification required",
)

_QUERY_STOPWORDS = {"service", "services", "system", "online", "software", "platform", "tools", "based"}


def _query_tokens(query):
    """Distinctive words from the query, used to reject generic legal boilerplate.

    Without this, a probe for unauthorized practice returns state bar pages for
    any query at all and every idea looks legally restricted.
    """
    return [t for t in re.findall(r"[a-z]{5,}", (query or "").lower()) if t not in _QUERY_STOPWORDS]


def _restriction_match(text, tokens):
    """(matched terms, matched query tokens) — a hit needs both."""
    blob = (text or "").lower()
    matched = [t for t in _RESTRICTION_TERMS if t in blob]
    overlap = [t for t in tokens if t in blob]
    return (matched, overlap) if (matched and overlap) else ([], [])


def _regulatory_search(query, limit=10):
    """Look for licensing or standing restrictions on selling this.

    Advisory, never a verdict: a hit means "read the statute", not "stop".
    Property tax appeals surfaced Illinois barring non-attorney representation
    while California does not regulate agents at all — same idea, different
    legal product shape per state.
    """

    import time
    tokens = _query_tokens(query)
    hits, flags, seen = [], set(), set()
    failed = 0
    probes = [
        f"{query} consultant license required represent client non-attorney",
        f"{query} unauthorized practice of law non-attorney",
    ]
    for i, probe in enumerate(probes):
        if i:
            time.sleep(2)  # DDG rate-limits bursts; a silent 0 would read as "clear"
        try:
            results = _web_search(probe, max_results=limit)
        except Exception:
            failed += 1
            continue
        for r in results:
            url = r.get("href", "")
            matched, _ = _restriction_match(f"{r.get('title', '')} {r.get('body', '')}", tokens)
            if not matched or url in seen:
                continue
            seen.add(url)
            flags.update(matched)
            hits.append({
                "title": (r.get("title") or "")[:100],
                "url": url,
                "matched": matched[:3],
                "snippet": (r.get("body") or "")[:200],
            })
    if hits:
        status = "restricted — verify the statute before building"
    elif failed == len(probes):
        status = "unknown — every regulatory search failed (rate limit?), absence of hits proves nothing"
    else:
        status = "no restriction signals found"
    return {
        "restriction_hits": len(hits),
        "restriction_terms": sorted(flags)[:6],
        "gov_sources": sum(1 for h in hits if _host(h["url"]).endswith(".gov")),
        "probes_failed": failed,
        "search_failed": failed == len(probes),
        "top_hits": hits[:4],
        "status": status,
    }


# ---------------------------------------------------------------------------
# Acquisition channel (who owns the buyer-intent results page)
# ---------------------------------------------------------------------------

_FORUM_HOSTS = ("reddit.com", "quora.com", "stackexchange.com", "news.ycombinator.com", "stackoverflow.com")


def _market_size_search(customer_group, limit=8, max_pages=4):
    """Snippets that may state how many of these customers exist, so the TAM can be cited instead
    of guessed. Searching the product query finds products, so this takes the customer group."""

    import time
    hits, failed = [], 0
    probes = [f"how many {customer_group} are there", f"number of {customer_group} statistics"]
    for i, probe in enumerate(probes):
        if i:
            time.sleep(2)  # DDG rate-limits bursts
        try:
            results = _web_search(probe, max_results=limit)
        except Exception:
            failed += 1
            continue
        hits += [{"title": (r.get("title") or "")[:120], "url": r.get("href", ""), "snippet": (r.get("body") or "")[:300]}
                 for r in results if r.get("href") and r.get("href") not in {h["url"] for h in hits}]
    # Snippets usually ask "how many ..." without the answer, so read the counts off the top pages.
    for h in hits[:max_pages]:
        h["snippet"] += " … " + " … ".join(_count_sentences(h["url"]))
    return {"results": hits, "search_failed": failed == len(probes)}


_COUNT_RE = re.compile(r"\d[\d,.]*\s*(?:million|billion|thousand|[mbk]\b)|\b\d{1,3}(?:,\d{3})+\b", re.IGNORECASE)


def _page_text(html):
    """Visible text: script and style contents (e.g. Next.js JSON full of "$24") are not prices or counts."""
    text = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", html)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))


def _count_sentences(url, limit=6):
    """Sentences on the page that state a count (e.g. "13.9 million", "250,000")."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (validation-tool)"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read(600_000).decode("utf-8", "ignore")
    except Exception:
        return []
    text = _page_text(html)
    return [m.group(0).strip()[:250] for m in re.finditer(r"[^.!?]{0,200}" + _COUNT_RE.pattern + r"[^.!?]{0,100}", text, re.IGNORECASE)][:limit]


def _classify_hosts(hosts, incumbent_hosts=()):
    """Bucket result hosts. Pure function so the read is testable offline."""
    buckets = {"vendor": 0, "government": 0, "forum": 0, "content": 0}
    for host in hosts:
        if not host:
            continue
        if host.endswith(".gov"):
            buckets["government"] += 1
        elif any(host == f or host.endswith("." + f) for f in _FORUM_HOSTS):
            buckets["forum"] += 1
        elif host in incumbent_hosts:
            buckets["vendor"] += 1
        else:
            buckets["content"] += 1
    total = sum(buckets.values()) or 1
    vendor_share = round(buckets["vendor"] / total, 2)
    return {
        "results_examined": sum(buckets.values()),
        "breakdown": buckets,
        "vendor_share": vendor_share,
        "read": (
            "vendors own the results page — paid acquisition is likely the only door"
            if vendor_share >= 0.3
            else "results page not vendor-dominated — organic entry plausible"
        ),
    }


def _serp_ownership(query, incumbent_hosts=(), limit=10):
    try:
        results = _web_search(query, max_results=limit)
    except Exception as e:
        return {"error": str(e)}
    hosts = [_host(r.get("href", "")) for r in results]
    out = _classify_hosts(hosts, incumbent_hosts)
    out["hosts"] = [h for h in hosts if h][:10]
    return out


def _fetch_pricing_prices(operators, max_pages=3):
    """Read prices off operators' own pricing pages rather than search snippets."""
    found = []
    for op in operators[:max_pages]:
        url = op.get("url", "")
        if not url:
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (validation-tool)"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read(400_000).decode("utf-8", "ignore")
        except Exception:
            continue
        text = _page_text(html)
        for p in _extract_prices([text])[:5]:
            i = text.find(p["raw"])
            found.append({**p, "source": op.get("host") or _host(url), "url": url,
                          "snippet": text[max(0, i - 80):i + 80] if i >= 0 else p["raw"]})
    return found


# ---------------------------------------------------------------------------
# Revenue signal helpers
# ---------------------------------------------------------------------------

_PRICE_RE = re.compile(
    r'\$\s*(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)\s*(?:per\s+)?(?:/\s*)?(mo(?:nth)?|yr|year|user|seat|month)?',
    re.IGNORECASE
)

def _extract_prices(texts):
    """Extract price mentions from a list of strings. Returns list of dicts.

    `period` records whether the source actually said per-month/per-year. A bare
    "$49" is recorded as "unknown", not assumed monthly — AppealDesk's $49 is a
    one-time fee, and treating it as $49/mo overstates revenue 12x.
    """
    found = []
    for text in texts:
        for m in _PRICE_RE.finditer(text or ""):
            amount = float(m.group(1).replace(",", ""))  # "$20,000" was read as $20
            raw_period = (m.group(2) or "").lower()
            if raw_period in ("yr", "year"):
                period, amount_mo = "annual", round(amount / 12, 2)
            elif raw_period in ("mo", "month", "user", "seat"):
                period, amount_mo = "monthly", amount
            else:
                period, amount_mo = "unknown", amount
            if 1 <= amount_mo <= 100_000:  # filter noise; one-time hardware (a $25,000 swim spa) is real
                found.append({"raw": m.group(0).strip(), "monthly_equiv": amount_mo, "period": period})
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


GROSS_MARGIN = 0.8              # software delivery; lower it for service businesses
MIN_EV_PER_CUSTOMER_USD = 200   # below this, paid acquisition rarely clears CAC
_CUSTOMERS_PER_MONTH = {"niche": 5, "mid": 20, "mass": 100}


def _unit_economics(prices, tam_tier):
    """Revenue from an observed price, not from search interest.

    The previous model picked an MRR range from the Google Trends tier alone,
    which is how a "Low" market signal could sit beside an ROI of 2500. Every
    number here traces to a named input, and when no competitor price is
    observed it returns nothing rather than inventing a range.
    """
    dated = sorted(p["monthly_equiv"] for p in (prices or []) if p.get("period") in ("monthly", "annual"))
    undated = sorted(p["monthly_equiv"] for p in (prices or []) if p.get("period") not in ("monthly", "annual"))

    if dated:
        anchor, recurring, basis = dated[len(dated) // 2], True, f"median of {len(dated)} prices with an explicit period"
    elif undated:
        anchor, recurring, basis = undated[len(undated) // 2], False, (
            f"median of {len(undated)} prices with no stated period — treated as one-time, not recurring"
        )
    else:
        anchor, recurring, basis = None, None, "no competitor price observed"

    if anchor is None:
        return {
            "price_anchor_usd": None,
            "price_is_recurring": None,
            "price_source": basis,
            "ev_per_customer_annual_usd": None,
            "below_acquisition_floor": None,
            "conservative_mrr": "",
            "optimistic_mrr": "",
            "note": "No observed price — revenue left unestimated rather than inferred from search volume.",
        }

    ev_annual = round(anchor * (12 if recurring else 1) * GROSS_MARGIN)
    base = _CUSTOMERS_PER_MONTH.get(tam_tier, 5)
    return {
        "price_anchor_usd": anchor,
        "price_is_recurring": recurring,
        "price_source": basis,
        "gross_margin_assumed": GROSS_MARGIN,
        "ev_per_customer_annual_usd": ev_annual,
        "price_observations": len(dated) if dated else len(undated),
        "acquisition_floor_usd": MIN_EV_PER_CUSTOMER_USD,
        "below_acquisition_floor": ev_annual < MIN_EV_PER_CUSTOMER_USD,
        "customers_assumed_per_month": {"conservative": base, "optimistic": base * 10},
        "conservative_mrr": f"${round(anchor * base)}",
        "optimistic_mrr": f"${round(anchor * base * 10)}",
        "note": (
            f"MRR = observed price (${anchor}{'/mo' if recurring else ' one-time'}) x assumed "
            f"customers/mo ({base} conservative, {base * 10} optimistic). The customer counts "
            f"are assumptions; the price is an observation."
        ),
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
    trends_result = {"skipped": True} if getattr(args, "skip_trends", False) else None
    for tq in ([] if trends_result else trends_queries):
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

    # Regulatory standing (advisory — never a verdict on its own)
    try:
        report["sources"]["regulatory"] = _regulatory_search(search_query)
    except Exception as e:
        report["sources"]["regulatory"] = {"error": str(e)}

    # Acquisition channel: who owns the buyer-intent results page
    try:
        inc_hosts = {o.get("host") for o in report["sources"].get("incumbents", {}).get("operators", [])}
        report["sources"]["serp_ownership"] = _serp_ownership(search_query, inc_hosts)
    except Exception as e:
        report["sources"]["serp_ownership"] = {"error": str(e)}

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
    try:
        competitor_prices += _fetch_pricing_prices(report["sources"].get("incumbents", {}).get("operators", []))
    except Exception:
        pass
    trends_avg = report["sources"].get("google_trends", {}).get("average_interest", 0)
    tam = _tam_tier(trends_avg)

    report["revenue_estimate"] = {
        "tam_tier": tam,
        "competitor_prices_found": competitor_prices,
        **_unit_economics(competitor_prices, tam),
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
    negatives = list(comp["negative"])

    reg = report["sources"].get("regulatory", {})
    if reg.get("restriction_hits", 0) > 0:
        terms = ", ".join(reg.get("restriction_terms", [])[:2])
        negatives.append(f"licensing/standing signals found ({terms}) — verify the statute")

    econ = report.get("revenue_estimate", {})
    if econ.get("below_acquisition_floor"):
        negatives.append(
            f"expected value ${econ['ev_per_customer_annual_usd']}/customer/yr is below "
            f"the ${MIN_EV_PER_CUSTOMER_USD} acquisition floor "
            f"({econ.get('price_observations', 0)} price observation(s))"
        )

    serp = report["sources"].get("serp_ownership", {})
    if serp.get("vendor_share", 0) >= 0.3:
        negatives.append("vendors own the buyer-intent results page — paid may be the only channel")

    # One observed price is too thin to kill an idea on; it stays a negative signal.
    if econ.get("below_acquisition_floor") and econ.get("price_observations", 0) >= 2:
        verdict = "unviable — value per customer below the acquisition floor"
    elif comp["level"] == "dominant":
        verdict = "crowded — a category owner already serves this market"
    elif comp["level"] == "crowded":
        verdict = "crowded — multiple vendors already selling"
    elif len(signals) >= 2:
        verdict = "validate further"
    else:
        verdict = "weak signal — reconsider or reframe"

    report["summary"] = {
        "positive_signals": signals,
        "negative_signals": negatives,
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
        _apply_claude_competition(report, claude_analysis)
        _category_competitors(report, claude_analysis)
        _source_price(args.query, report, claude_analysis)
        _source_tam(report, claude_analysis)
        _discount_unsourced_tam(claude_analysis)
        _annualize_one_time(claude_analysis)

    if getattr(args, "require_brave", False) and (_brave_refused or not os.environ.get("BRAVE_API_KEY")):
        sys.stderr.write(f"Brave search refused (HTTP {sorted(set(_brave_refused))}); report discarded\n")
        sys.exit(EXIT_SEARCH_REFUSED)
    print(json.dumps(report, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Claude revenue/value synthesis
# ---------------------------------------------------------------------------

COMPETITION_LEVELS = ("dominant", "crowded", "funded", "contested", "open", "none_found")


def _source_texts(sources, out=None):
    """url -> title + snippet for every item in the research data, at any depth."""
    out = {} if out is None else out
    if isinstance(sources, dict):
        url = sources.get("url")
        if isinstance(url, str):
            out[url] = " ".join(str(sources.get(k, "")) for k in ("title", "name", "headline", "snippet")).lower()
        for v in sources.values():
            _source_texts(v, out)
    elif isinstance(sources, list):
        for v in sources:
            _source_texts(v, out)
    return out


def _apply_claude_competition(report, analysis):
    """Replace the heuristic competition grade with Claude's, keeping only competitors whose cited
    snippet names them, and redo the competition branch of the verdict."""
    level = analysis.get("competition_level")
    if level not in COMPETITION_LEVELS:
        return
    cited = _cited(analysis.get("competitors"), _source_texts(report.get("sources", {})))
    analysis["competitors"] = cited
    if level != "none_found" and not cited:
        return  # a grade with no competitor the data backs is not evidence
    s = report["summary"]
    s["competition_heuristic"], s["competition"] = s["competition"], level
    _competition_verdict(s, level)


def _cited(competitors, texts):
    """Competitors whose evidence_url's title or snippet names them, as {name, evidence_url, funding_usd}."""
    return [{k: c.get(k) for k in ("name", "evidence_url", "why", "funding_usd")} for c in competitors or []
            if isinstance(c, dict) and c.get("name") and c["name"].lower() in texts.get(c.get("evidence_url"), "")]


def _category_competitors(report, analysis):
    """The Validation Query is often narrow ("predict forex from import/export data") and its results miss rivals
    selling to the same buyers, so also search the category they would shop in and cite the vendors it names."""
    category = analysis.get("product_category")
    if not category:
        return
    try:
        hits = _web_search(f"best {category}", max_results=10)
    except Exception:
        return
    results = [{"url": h.get("href"), "title": h.get("title", ""), "snippet": (h.get("body") or "")[:300]} for h in hits]
    report["sources"]["category_search"] = {"query": f"best {category}", "results": results}
    found = _claude_json(f"""Product category: {category}. Buyers: {analysis.get("customer_group") or "unknown"}.
Search results: {json.dumps(results, ensure_ascii=False)}
Product idea: {report.get("query")}.
List up to 8 competitors that a result's title or snippet names — products or companies, NOT blogs, review or
comparison sites, directories or papers. A competitor sells the same kind of product, one these buyers would compare against this idea; adjacent markets
don't count (for neighbors selling home-cooked food, restaurant delivery apps and meal kits are not competitors).
Return only JSON {{"competitors": [{{"name": str, "evidence_url": the url of the result naming it, "why": what it sells, in
a few words, "funding_usd": total raised if you know it, else null}}]}}""") or {}
    merge_competitors(report, analysis, _cited(found.get("competitors"), _source_texts(results)))


COMPETITION_SEVERITY = ("none_found", "open", "contested", "funded", "crowded", "dominant")
CROWDED_COMPETITORS = 5  # cited vendors, so unlike CROWDED_OPERATORS no review-site noise; matches the prompt's "5+"


def _competitors_level(competitors):
    """The grade the review prompt defines, computed from the cited competitors' count and funding."""
    n = len(competitors)
    funding = max((c["funding_usd"] for c in competitors if isinstance(c.get("funding_usd"), (int, float))), default=0)
    if funding >= DOMINANT_FUNDING_USD:
        return "dominant"
    if funding >= FUNDED_FUNDING_USD:
        return "crowded" if n >= CROWDED_COMPETITORS else "funded"
    return "crowded" if n >= CROWDED_COMPETITORS else "contested" if n >= 2 else "open" if n else "none_found"


def merge_competitors(report, analysis, more):
    """Add competitors not already listed (by name) and raise the grade, verdict and probability ceiling to what
    the combined list implies. Never lowers the grade: one run's search missing a vendor doesn't remove it."""
    names = {c["name"].lower() for c in analysis.get("competitors") or []}
    new = [c for c in more if c["name"].lower() not in names and not names.add(c["name"].lower())]
    analysis["competitors"] = (analysis.get("competitors") or []) + new
    s = report.setdefault("summary", {})
    level, current = _competitors_level(analysis["competitors"]), s.get("competition")
    if COMPETITION_SEVERITY.index(level) <= COMPETITION_SEVERITY.index(current if current in COMPETITION_SEVERITY else "none_found"):
        return
    s["competition"] = level
    _competition_verdict(s, level)
    cap = 0.01 if level == "dominant" else 0.1 if level in ("funded", "crowded") else None  # the prompt's ceilings
    if cap and isinstance(analysis.get("suggested_probability"), (int, float)):
        analysis["suggested_probability"] = min(analysis["suggested_probability"], cap)


def _competition_verdict(s, level):
    if s.get("verdict", "").startswith("unviable"):
        return
    if level == "dominant":
        s["verdict"] = "crowded — a category owner already serves this market"
    elif level == "crowded":
        s["verdict"] = "crowded — multiple vendors already selling"
    else:
        s["verdict"] = "validate further" if s.get("signal_count", 0) >= 2 else "weak signal — reconsider or reframe"


TAM_SHARES = {"100%": 1.0, "10%": 0.1, "1%": 0.01, "0.1%": 0.001}


def _source_tam(report, analysis):
    """Search for a count of analysis["customer_group"] and have Claude cite one. A verified count is the
    population, usually broader than the buyers ("4.3 million small businesses"), so TAM = population x a
    share tier Claude picks in a narrow call; that call gave the same tier 3/3 runs on 10/10 ideas, unlike
    the open-ended review. Otherwise the TAM stays a guess and tam_sourced is False."""
    analysis["tam_sourced"] = False
    group = analysis.get("customer_group")
    if not group:
        return
    try:
        report["sources"]["market_size"] = ms = _market_size_search(group)
    except Exception as e:
        report["sources"]["market_size"] = {"error": str(e)}
        return
    if not ms["results"]:
        return
    cite = _claude_json(f"""Below are search results. Find the one that states how many {group} exist (a count of
people or businesses, not revenue, not a different population, not a percentage).

{json.dumps(ms["results"], indent=1, ensure_ascii=False)}

Return only JSON: {{"tam_source": that result's url or null, "tam_source_quote": the count exactly as written in its
title or snippet (e.g. "13.9 million") or null, "count": the count as a plain integer or null}}""") or {}
    analysis.update({k: cite.get(k) for k in ("tam_source", "tam_source_quote")})
    _apply_tam_source(report, analysis)
    count = cite.get("count")
    if not (analysis["tam_sourced"] and isinstance(count, (int, float)) and count > 0):
        analysis["tam_sourced"] = False
        return
    share = _claude_json(f"""Product idea: {report.get("query")}. Population: {cite["tam_source_quote"]} {group}.
What share of this population would plausibly pay for this product? Choose exactly one of {list(TAM_SHARES)}.
Return only JSON {{"share": one of those strings, "reason": one short clause on who within the population buys}}""") or {}
    if share.get("share") not in TAM_SHARES:
        analysis["tam_sourced"] = False  # a population without a share is not a TAM
        return
    tam = count * TAM_SHARES[share["share"]]
    analysis.update(tam_guess=analysis.get("tam_customers"), tam_population=int(count), tam_share=share["share"], tam_share_reason=share.get("reason"),
                    tam_customers=round_oom(tam))
    price = analysis.get("price_per_customer_annual")
    if isinstance(price, (int, float)) and price > 0:
        analysis["value"] = round_oom(analysis["tam_customers"] * price)


def _source_price(query, report, analysis):
    """Have Claude cite a comparable vendor price from the research data; _apply_price_source verifies it.
    The main review prices from memory as often as from the data, so citing is a separate, narrow ask."""
    analysis["price_sourced"] = False
    texts = _source_texts([report.get("sources", {}), report.get("revenue_estimate", {})])
    priced = {u: t[max(0, t.find("$") - 150):t.find("$") + 250] for u, t in texts.items() if "$" in t}
    if not priced or not analysis.get("price_per_customer_annual"):
        return
    cite = _claude_json(f"""Product idea: {query}. Paying customers: {analysis.get("customer_group") or "unknown"}.
Below are research excerpts by URL. Find one that states a price a vendor charges these customers for a comparable
product (not an ad rate, salary, API token rate or market statistic).

{json.dumps(dict(list(priced.items())[:20]), indent=1, ensure_ascii=False)}

Return only JSON: {{"price_source": that URL or null, "price_source_quote": the price exactly as written in its
excerpt (e.g. "$49/month") or null}}""") or {}
    analysis.update({k: cite.get(k) for k in ("price_source", "price_source_quote")})
    _apply_price_source(report, analysis)


def round_oom(v):
    """Nearest power of 10 on a log scale (430,000 -> 1,000,000; 300,000 -> 100,000), like Claude's own estimates."""
    return int(10 ** round(math.log10(v)))


TAM_GUESS_DISCOUNT = 10  # 2026-10-06: on 16 ideas with a sourced TAM, Claude's guess was a median 25x higher
                         # (14x excluding 2 sourced counts of the wrong population); 10 is the cautious end


def _discount_unsourced_tam(analysis):
    """An unsourced TAM is Claude's guess divided by TAM_GUESS_DISCOUNT; tam_guess keeps the guess."""
    tam = analysis.get("tam_customers")
    if analysis.get("tam_sourced") or not isinstance(tam, (int, float)) or tam <= 0:
        return
    analysis["tam_guess"] = tam
    analysis["tam_customers"] = max(1, int(tam / TAM_GUESS_DISCOUNT))


def _annualize_one_time(analysis):
    """Notion's Value multiplies price/yr by 10 years, so a one-time sale (hardware) is stored as a tenth of its
    price; price_one_time keeps the real figure. Runs after the price citation, which compares the real price."""
    price = analysis.get("price_per_customer_annual")
    if analysis.get("price_type") == "one_time" and isinstance(price, (int, float)) and price > 0:
        analysis["price_one_time"] = price
        analysis["price_per_customer_annual"] = price / 10


def _apply_price_source(report, analysis):
    """price_sourced: the cited quote is in the cited page and price_per_customer_annual is within 10x of it
    annualized (seats or tiers can legitimately differ, an invented $10,000/yr against a $20/mo quote cannot)."""
    texts = _source_texts([report.get("sources", {}), report.get("revenue_estimate", {})])
    url, quote, price = analysis.get("price_source"), analysis.get("price_source_quote"), analysis.get("price_per_customer_annual")
    squash = lambda t: re.sub(r"\s+", "", str(t).lower())
    parsed = _extract_prices([str(quote or "")])
    ok = bool(url and quote and parsed and isinstance(price, (int, float)) and price > 0
              and squash(quote) in squash(texts.get(url, "")))
    if ok:
        q, words = parsed[0], str(quote).lower()
        monthly = q["period"] in ("monthly", "annual") or re.search(r"month|/\s*mo\b", words)  # "$25 per screen per month"
        annual = q["monthly_equiv"] * 12 if monthly else q["monthly_equiv"]
        ok = 0.1 <= price / annual <= 10
    if not ok:
        analysis["price_source"] = analysis["price_source_quote"] = None
    analysis["price_sourced"] = ok


def _apply_tam_source(report, analysis):
    """Keep tam_source only if its snippet contains the quoted count; tam_sourced flags the rest as assumed."""
    texts = _source_texts(report.get("sources", {}))
    url, quote = analysis.get("tam_source"), analysis.get("tam_source_quote")
    squash = lambda t: re.sub(r"\s+", "", str(t).lower())  # DDG snippets drop spaces around bolded terms
    ok = bool(url and quote and any(c.isdigit() for c in str(quote)) and squash(quote) in squash(texts.get(url, "")))
    if not ok:
        analysis["tam_source"] = analysis["tam_source_quote"] = None
    analysis["tam_sourced"] = ok


def _claude_review(query, report, assume_tech_exists=False):
    """Call Claude to synthesize the report data into a revenue/value estimate."""
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

Revenue signals extracted (the price anchor is an OBSERVED competitor price; customer counts are assumptions):
{json.dumps(report.get("revenue_estimate", {}), indent=2)}

Competition and standing (summary):
{json.dumps(report.get("summary", {}), indent=2)}
summary.competition is a keyword heuristic: it counts any pricing-page host as a vendor (including review blogs and
comparison sites) and misses funding when a search fails. Grade competition yourself in "competition_level".

All numeric outputs must be rounded to the nearest power of 10 (e.g. 100, 1000, 10000, 100000, 1000000). Do not use precise figures — order-of-magnitude accuracy is the goal.

Provide your assessment as JSON with these fields:
- "tam_assessment": one sentence on market size (mention specific evidence from the data)
- "tam_customers": estimated number of potential customers, rounded to nearest power of 10
- "customer_group": the paying customers in 2-5 words, as a searchable noun phrase (e.g. "retail forex traders")
- "product_category": the narrowest category naming this kind of product, in 2-4 words, as buyers would search for it
  (e.g. "forex signals software"; "home cooked meal marketplace", not "food delivery")
- "price_type": "one_time" if customers pay once (hardware, a one-off purchase), else "recurring"
- "price_per_customer_annual": estimated annual revenue per customer in USD (for "one_time", the one-time price), rounded to nearest power of 10 (e.g. 100 for ~$8-12/mo, 1000 for ~$80-120/mo)
- "pricing_assessment": one sentence on pricing strategy and willingness to pay (e.g. "B2B SaaS at ~$100/yr is realistic given competitor pricing")
- "legal_status": one of "clear" | "restricted" | "unknown" — whether licensing or standing rules limit who may sell this, based on the regulatory source
- "legal_reasoning": one sentence citing the specific restriction found, or stating that none surfaced
- "key_risks": list of 2-3 main risks to revenue (exclude technical feasibility risk)
- "key_opportunities": list of 2-3 strongest signals supporting the idea
- "value": total addressable annual revenue in USD, rounded to nearest power of 10 — this is the FULL market potential (tam_customers × price_per_customer_annual), with NO adjustment for penetration or probability. Do not discount for competition or execution risk here.
- "value_reasoning": one sentence explaining the value estimate (reference tam_customers × price_per_customer_annual)
- "competitors": up to 5 actual vendors named in the research data above — products or companies, NOT blogs, review
  or comparison sites, directories or papers. A competitor sells the same kind of product, one these buyers would compare against this idea; adjacent markets
  don't count (for neighbors selling home-cooked food, restaurant delivery apps and meal kits are not competitors).
  Each: {{"name": str, "evidence_url": the research-data URL whose title or snippet names it, "why": what it sells, in
  a few words, "funding_usd": total raised if you know it, else null}}
- "competition_level": one of
    "dominant" — a competitor has raised >= $100M or is a big-tech product
    "crowded" — 5+ vendors selling, or a funded competitor among several
    "funded" — a competitor has raised >= $10M
    "contested" — 2-4 small vendors
    "open" — 1 vendor
    "none_found" — no vendor named in the data
- "suggested_probability": expected fraction of the total value that will actually be captured, using exactly one of these three values:
    0.01 — moonshot: paradigm shift required, or tiny realistic penetration (e.g. <1% of a niche market)
    0.10 — regular challenge: real demand and proven tech, but significant competition or execution risk (realistic penetration ~5-15%)
    0.99 — low-hanging fruit: clear unmet demand, proven solution, little competition (high penetration likely)
  This encodes both probability of success AND realistic market penetration. Choose the closest tier.
  Ceilings by evidence (apply the lowest that matches):
    competition_level == "dominant" -> do not exceed 0.01
    competition_level in ("funded", "crowded") -> do not exceed 0.10
    legal_status == "restricted" -> do not exceed 0.10
    revenue_estimate.below_acquisition_floor is true AND price_observations >= 2 -> do not exceed 0.01
  A funded competitor is evidence the market is real; it caps the upside, it does not zero it. Competition levels "contested" and "open" carry no ceiling.
- "probability_reasoning": one sentence explaining the probability choice, including the expected penetration rate

Return only valid JSON, no markdown."""
    return _claude_json(prompt)


def _claude_json(prompt):
    """JSON from Claude: the Anthropic API for the paid web app (VALIDATION_LLM=api), else the Claude Code CLI."""
    import subprocess
    import shutil

    if os.environ.get("VALIDATION_LLM") == "api":
        return _claude_api_json(prompt)
    claude_path = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    if not os.path.exists(claude_path):
        return None

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


def _claude_api_json(prompt):
    """Same review through the Anthropic API — used by the paid web app (VALIDATION_LLM=api),
    where the personal Claude Code subscription must not serve customers."""
    import anthropic

    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY
    try:
        response = client.beta.messages.create(
            model="claude-opus-5",
            max_tokens=16000,
            output_config={"effort": "medium"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIStatusError as e:
        return {"error": f"Claude API {e.status_code}: {e.message}"}
    except anthropic.APIConnectionError as e:
        return {"error": f"Claude API connection error: {e}"}
    if response.stop_reason == "refusal":
        return {"error": "Claude declined to assess this idea"}
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    if text.startswith("```"):
        text = "\n".join(text.split("\n")[1:]).rsplit("```", 1)[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Claude returned unparseable JSON"}


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

    p_reg = subparsers.add_parser("regulatory", help="Search for licensing / standing restrictions")
    p_reg.add_argument("--query", required=True)

    p_serp = subparsers.add_parser("serp", help="Who owns the buyer-intent results page")
    p_serp.add_argument("--query", required=True)
    p_serp.add_argument("--limit", type=int, default=10)

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
    p_report.add_argument("--require-brave", action="store_true",
                          help=f"Exit {EXIT_SEARCH_REFUSED} with no report if Brave refuses any search (batch runs resume instead of mixing in ddgs)")
    p_report.add_argument("--skip-trends", action="store_true",
                          help="Skip Google Trends (it rate-limits batch runs); trends-based fields are then meaningless")
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
    elif args.command == "regulatory":
        print(json.dumps(_regulatory_search(args.query), indent=2, ensure_ascii=False))
    elif args.command == "serp":
        print(json.dumps(_serp_ownership(args.query, limit=args.limit), indent=2, ensure_ascii=False))
    elif args.command == "reddit":
        cmd_reddit(args)
    elif args.command == "report":
        cmd_report(args)


if __name__ == "__main__":
    main()
