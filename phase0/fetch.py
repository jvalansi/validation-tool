#!/usr/bin/env python3
"""
Collect raw discussion items for one niche into data/<niche>/raw.jsonl.

A niche is niches/<name>.json:
  {"subreddits": [...], "github_repos": [...], "discourse": [...], "hn_queries": [...], "workaround_queries": [...],
   "app_queries": [...], "podcast_queries": [...]}
All keys optional. Each item: {id, source, title, body, engagement, url, created}.

Reddit gets top posts plus pain-phrase searches ("is there a tool", "I hate", ...),
which surface complaints far more densely than top posts alone.
workaround_queries search Upwork and Freelancer.com job posts: people already paying someone to do a task by hand.
app_queries find the audience's tools on Google Play and take their recent 1-2 star reviews (G2, Capterra and
TrustRadius return 403). podcast_queries find podcasts that publish transcripts and keep transcript chunks with pain phrases.

Usage: python fetch.py <niche> [source ...]
  With sources (e.g. `upwork freelancer`), fetches only those and merges them into the existing raw.jsonl.
Reddit goes through rdt-cli, which needs a logged-in reddit_session cookie in
~/.config/rdt-cli/credential.json (see README).
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RDT = os.path.join(os.path.dirname(sys.executable), "rdt")
BODY_CHARS = 1500
PAIN_QUERIES = ['"is there a tool"', '"is there software"', '"I hate"', '"so tedious"',
                '"wish there was"', "spreadsheet", '"manually"', '"would pay"']


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "opportunity-scout/0.2", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def github(repos):
    token = os.environ.get("GH_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    for repo in repos:
        for page in (1, 2):
            url = f"https://api.github.com/repos/{repo}/issues?state=all&sort=comments&direction=desc&per_page=100&page={page}"
            try:
                issues = get_json(url, headers)
            except Exception as e:
                print(f"github {repo} p{page}: {e}", file=sys.stderr)
                break
            for i in issues:
                if "pull_request" in i:
                    continue
                yield {
                    "id": f"gh:{repo}#{i['number']}", "source": f"github:{repo}", "title": i["title"],
                    "body": (i.get("body") or "")[:BODY_CHARS],
                    "engagement": i["comments"] + i.get("reactions", {}).get("total_count", 0),
                    "url": i["html_url"], "created": i["created_at"][:10],
                }


def _reddit_item(d, sub):
    return {
        "id": f"rd:{d['id']}", "source": f"reddit:r/{sub}", "title": d["title"],
        "body": (d.get("selftext") or "")[:BODY_CHARS], "engagement": d["score"] + d["num_comments"],
        "url": "https://www.reddit.com" + d["permalink"],
        "created": time.strftime("%Y-%m-%d", time.gmtime(d["created_utc"])),
    }


def reddit_via_search(subreddits):
    """Fallback when the Reddit API is unreachable: titles + snippets via DuckDuckGo site: search.
    Thinner than the API (no bodies or scores), but needs no token or proxy."""
    from ddgs import DDGS
    for sub in subreddits:
        seen = set()
        for q in PAIN_QUERIES:
            try:
                hits = list(DDGS().text(f"site:reddit.com/r/{sub} {q}", max_results=20))
            except Exception as e:
                print(f"ddg {sub} {q}: {e}", file=sys.stderr)
                time.sleep(5)
                continue
            for h in hits:
                m = re.search(r"/comments/([a-z0-9]+)", h.get("href", ""))
                if not m or m.group(1) in seen:
                    continue
                seen.add(m.group(1))
                yield {"id": f"rd:{m.group(1)}", "source": f"reddit:r/{sub}", "title": h.get("title", ""),
                       "body": h.get("body", "")[:BODY_CHARS], "engagement": 0, "url": h["href"], "created": ""}
            time.sleep(2)


def _upwork_item(h):
    """A search hit → item, or None if it isn't a single job post."""
    m = re.search(r"upwork\.com/freelance-jobs/apply/[^/]*_~(\d+)", h.get("href", ""))
    if not m or h.get("body", "").startswith("Find & apply"):  # generic page text, not the post
        return None
    title = re.sub(r"\s*-\s*(Freelance Job.*|Upwork)$", "", h.get("title", ""))
    return {"id": f"uw:{m.group(1)}", "source": "upwork", "title": title, "body": h["body"][:BODY_CHARS],
            "engagement": 0, "url": h["href"], "created": ""}


def upwork(queries):
    """Upwork job posts via Bing/Yahoo site: search (Upwork returns 403 to direct requests).
    Titles + snippets only, ~7 hits per query; DuckDuckGo's own backend returns none for this site."""
    from ddgs import DDGS
    for q in queries:
        for attempt in (1, 2):
            try:
                hits = DDGS().text(f"site:upwork.com/freelance-jobs/apply {q}", max_results=30, backend="bing,yahoo")
                break
            except Exception as e:
                print(f"upwork {q} (try {attempt}): {e}", file=sys.stderr)
                hits = []
                time.sleep(5)
        for h in hits:
            item = _upwork_item(h)
            if item:
                yield item
        time.sleep(2)


def _freelancer_item(p):
    b = p.get("budget") or {}
    budget = f"{b.get('minimum') or 0:g}-{b.get('maximum') or 0:g} {p['currency']['code']} {p.get('type', '')}"
    bids = (p.get("bid_stats") or {}).get("bid_count") or 0
    return {"id": f"fl:{p['id']}", "source": "freelancer", "title": p["title"],
            "body": f"Budget {budget}, {bids} bids. {p.get('description') or ''}"[:BODY_CHARS], "engagement": bids,
            "url": f"https://www.freelancer.com/projects/{p['seo_url']}",
            "created": time.strftime("%Y-%m-%d", time.gmtime(p["time_submitted"]))}


def freelancer(queries):
    """Active Freelancer.com projects from its public API (no key): full description, budget, bid count."""
    for q in queries:
        url = "https://www.freelancer.com/api/projects/0.1/projects/active/?" + urllib.parse.urlencode(
            {"query": q, "limit": 30, "full_description": "true"})
        try:
            projects = get_json(url)["result"]["projects"]
        except Exception as e:
            print(f"freelancer {q}: {e}", file=sys.stderr)
            continue
        for p in projects:
            yield _freelancer_item(p)
        time.sleep(1)


def google_play(queries, apps_per_query=3, per_app=20):
    from google_play_scraper import Sort, reviews, search
    seen = set()
    for q in queries:
        try:
            apps = [a for a in search(q, n_hits=apps_per_query) if a.get("appId")]
        except Exception as e:
            print(f"play search {q}: {e}", file=sys.stderr)
            continue
        for a in apps:
            if a["appId"] in seen:
                continue
            seen.add(a["appId"])
            for stars in (1, 2):
                try:
                    rv, _ = reviews(a["appId"], sort=Sort.NEWEST, count=per_app, filter_score_with=stars)
                except Exception as e:
                    print(f"play reviews {a['appId']}: {e}", file=sys.stderr)
                    continue
                for r in rv:
                    if len(r.get("content") or "") < 80:  # "this app sucks" says nothing about the work
                        continue
                    yield {"id": f"gp:{r['reviewId']}", "source": f"play:{a['appId']}",
                           "title": f"{a['title']} review ({stars}★)", "body": r["content"][:BODY_CHARS],
                           "engagement": r.get("thumbsUpCount") or 0,
                           "url": f"https://play.google.com/store/apps/details?id={a['appId']}",
                           "created": str(r.get("at") or "")[:10]}
            time.sleep(1)


PAIN_RE = re.compile(r"\b(hate|frustrat|annoying|tedious|manual(ly)?|spreadsheet|nightmare|painful|waste|"
                     r"wish there|no tool|can't find|struggl|headache|takes forever|hours)", re.I)


def transcript_chunks(text, size=1200):
    """Split a transcript into ~size-char windows and keep those with a pain phrase."""
    words, chunks, cur = text.split(), [], []
    for w in words:
        cur.append(w)
        if sum(len(x) + 1 for x in cur) >= size:
            chunks.append(" ".join(cur))
            cur = []
    if cur:
        chunks.append(" ".join(cur))
    return [(i, c) for i, c in enumerate(chunks) if PAIN_RE.search(c)]


def transcript_text(raw):
    """SRT / VTT / HTML / JSON transcript → plain text (drops cue numbers, timestamps, tags)."""
    try:
        d = json.loads(raw)
        return " ".join(seg.get("body", "") for seg in d.get("segments", []))
    except ValueError:
        pass
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = re.sub(r"(?m)^(WEBVTT.*|\d+|[\d:.,]+ --> [\d:.,]+.*)$", " ", raw)
    return re.sub(r"\s+", " ", raw).strip()


def podcasts(queries, shows=25, episodes_per_show=3, chunks_per_episode=8):
    """Podcasts found via the iTunes search API whose RSS feeds publish <podcast:transcript>
    (Buzzsprout, Spreaker, RSS.com ...; roughly 1 show in 5) → transcript chunks with pain phrases.
    YouTube was tried first and blocks this server's transcript requests."""
    seen = set()
    for q in queries:
        url = "https://itunes.apple.com/search?" + urllib.parse.urlencode({"term": q, "media": "podcast", "limit": shows})
        try:
            results = get_json(url)["results"]
        except Exception as e:
            print(f"podcast search {q}: {e}", file=sys.stderr)
            continue
        for show in results:
            if not show.get("feedUrl") or show["collectionId"] in seen:
                continue
            seen.add(show["collectionId"])
            try:
                req = urllib.request.Request(show["feedUrl"], headers={"User-Agent": "Mozilla/5.0"})
                feed = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
            except Exception as e:
                print(f"podcast feed {show['collectionName']}: {e}", file=sys.stderr)
                continue
            n = 0
            for item in re.findall(r"<item>.*?</item>", feed, re.S):
                t = re.search(r'<podcast:transcript[^>]*url="([^"]+)"', item)
                if not t:
                    continue
                title = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", item, re.S)
                guid = re.sub(r"\W", "", t.group(1))[-40:]
                try:
                    req = urllib.request.Request(t.group(1).replace("&amp;", "&"), headers={"User-Agent": "Mozilla/5.0"})
                    text = transcript_text(urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore"))
                except Exception as e:
                    print(f"transcript {t.group(1)[:60]}: {e}", file=sys.stderr)
                    continue
                for i, c in transcript_chunks(text)[:chunks_per_episode]:
                    yield {"id": f"pc:{guid}:{i}", "source": "podcast",
                           "title": f"{show['collectionName']}: {title.group(1).strip() if title else ''}",
                           "body": c[:BODY_CHARS], "engagement": 0, "url": show.get("collectionViewUrl", ""),
                           "created": ""}
                n += 1
                if n == episodes_per_show:
                    break


def rdt(*args):
    """Run rdt-cli and return the listing's children. Raises on auth/network failure."""
    out = subprocess.run([RDT, *args, "--json"], capture_output=True, text=True, timeout=120)
    d = json.loads(out.stdout or "{}")
    if not d.get("ok"):
        raise RuntimeError((d.get("error") or {}).get("message") or out.stderr.strip()[-200:])
    return d["data"]["data"]["children"]


def reddit(subreddits):
    try:
        rdt("search", "tool", "-n", "1")
    except Exception as e:
        print(f"rdt-cli unavailable ({e}) — using search fallback", file=sys.stderr)
        yield from reddit_via_search(subreddits)
        return
    for sub in subreddits:
        calls = [("sub", sub, "-s", "top", "-t", "year", "-n", "100")] + [
            ("search", q, "-r", sub, "-s", "top", "-t", "all", "-n", "25") for q in PAIN_QUERIES]
        seen = set()
        for args in calls:
            try:
                children = rdt(*args)
            except Exception as e:
                print(f"reddit {sub} {args[1][:30]}: {e}", file=sys.stderr)
                continue
            for c in children:
                if c["data"]["id"] not in seen:
                    seen.add(c["data"]["id"])
                    yield _reddit_item(c["data"], sub)
            time.sleep(1)


def hacker_news(queries):
    for q in queries:
        url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
            {"query": q, "tags": "(story,ask_hn)", "hitsPerPage": 50})
        try:
            hits = get_json(url)["hits"]
        except Exception as e:
            print(f"hn {q}: {e}", file=sys.stderr)
            continue
        for h in hits:
            yield {
                "id": f"hn:{h['objectID']}", "source": "hackernews", "title": h.get("title") or "",
                "body": re.sub(r"<[^>]+>", " ", h.get("story_text") or "")[:BODY_CHARS],
                "engagement": (h.get("points") or 0) + (h.get("num_comments") or 0),
                "url": f"https://news.ycombinator.com/item?id={h['objectID']}", "created": h["created_at"][:10],
            }


def discourse(bases, pages=8):
    for base in bases:
        seen, topics = set(), []
        for url in [f"{base}/top.json?period=all"] + [f"{base}/latest.json?page={p}" for p in range(pages)]:
            try:
                topics += get_json(url)["topic_list"]["topics"]
            except Exception as e:
                print(f"discourse {url}: {e}", file=sys.stderr)
        for t in topics:
            if t["id"] in seen:
                continue
            seen.add(t["id"])
            try:
                full = get_json(f"{base}/t/{t['id']}.json")
                body = re.sub(r"<[^>]+>", " ", full["post_stream"]["posts"][0]["cooked"])
            except Exception as e:
                print(f"discourse topic {t['id']}: {e}", file=sys.stderr)
                body = ""
            time.sleep(0.3)
            yield {
                "id": f"dc:{base.split('//')[-1]}:{t['id']}", "source": f"discourse:{base.split('//')[-1]}",
                "title": t["title"], "body": re.sub(r"\s+", " ", body)[:BODY_CHARS],
                "engagement": t.get("posts_count", 0) + t.get("like_count", 0),
                "url": f"{base}/t/{t['slug']}/{t['id']}", "created": t["created_at"][:10],
            }


def main():
    niche, only = sys.argv[1], sys.argv[2:]
    cfg = json.load(open(os.path.join(HERE, "niches", f"{niche}.json")))
    out_dir = os.path.join(HERE, "data", niche)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "raw.jsonl")
    if only and not os.path.exists(out):  # sweep.py only fetches niches with no raw.jsonl, so this would stick
        sys.exit(f"{out} missing: run a full fetch before merging {only} into it")
    counts, ids = {}, set()
    with open(out + ".tmp", "w") as f:
        if only:
            for line in open(out):
                ids.add(json.loads(line)["id"])
                f.write(line)
        for name, gen in (("github", lambda: github(cfg.get("github_repos", []))),
                          ("reddit", lambda: reddit(cfg.get("subreddits", []))),
                          ("hackernews", lambda: hacker_news(cfg.get("hn_queries", []))),
                          ("discourse", lambda: discourse(cfg.get("discourse", []))),
                          ("upwork", lambda: upwork(cfg.get("workaround_queries", []))),
                          ("freelancer", lambda: freelancer(cfg.get("workaround_queries", []))),
                          ("play", lambda: google_play(cfg.get("app_queries", []))),
                          ("podcast", lambda: podcasts(cfg.get("podcast_queries", [])))):
            if only and name not in only:
                continue
            for item in gen():
                if item["id"] in ids:
                    continue
                ids.add(item["id"])
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                counts[name] = counts.get(name, 0) + 1
            print(f"{niche} {name}: {counts.get(name, 0)} items", file=sys.stderr)
    os.replace(out + ".tmp", out)


if __name__ == "__main__":
    main()
