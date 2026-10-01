#!/usr/bin/env python3
"""
Collect raw discussion items for one niche into data/<niche>/raw.jsonl.

A niche is niches/<name>.json:
  {"subreddits": [...], "github_repos": [...], "discourse": [...], "hn_queries": [...]}
All keys optional. Each item: {id, source, title, body, engagement, url, created}.

Reddit gets top posts plus pain-phrase searches ("is there a tool", "I hate", ...),
which surface complaints far more densely than top posts alone.

Usage: python fetch.py <niche>
Reddit needs a fresh token: /home/ubuntu/miniconda3/bin/python ../../reddit-tool/refresh_token.py
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "reddit-tool"))
from reddit_playwright import api as reddit_api  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
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


def reddit(subreddits):
    try:
        reddit_api("GET", "/api/v1/me")
    except Exception as e:
        print(f"reddit API unavailable ({e}) — using search fallback", file=sys.stderr)
        yield from reddit_via_search(subreddits)
        return
    for sub in subreddits:
        paths = [f"/r/{sub}/top?t=year&limit=100"] + [
            f"/r/{sub}/search?q={urllib.parse.quote(q)}&restrict_sr=1&sort=top&t=all&limit=25" for q in PAIN_QUERIES]
        seen = set()
        for path in paths:
            try:
                data = reddit_api("GET", path)
            except Exception as e:
                print(f"reddit {sub} {path[:40]}: {e}", file=sys.stderr)
                continue
            for c in data.get("data", {}).get("children", []):
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
    niche = sys.argv[1]
    cfg = json.load(open(os.path.join(HERE, "niches", f"{niche}.json")))
    out_dir = os.path.join(HERE, "data", niche)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "raw.jsonl")
    counts, ids = {}, set()
    with open(out + ".tmp", "w") as f:
        for name, gen in (("github", lambda: github(cfg.get("github_repos", []))),
                          ("reddit", lambda: reddit(cfg.get("subreddits", []))),
                          ("hackernews", lambda: hacker_news(cfg.get("hn_queries", []))),
                          ("discourse", lambda: discourse(cfg.get("discourse", [])))):
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
