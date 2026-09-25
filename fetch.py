#!/usr/bin/env python3
"""
Collect raw BCI/neurotech discussion items (GitHub issues, Reddit posts, MNE forum topics)
into data/raw.jsonl. Each item: {id, source, title, body, engagement, url, created}.

Usage: python fetch.py
Reddit needs a fresh token: /home/ubuntu/miniconda3/bin/python ../reddit-tool/refresh_token.py
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "reddit-tool"))
from reddit_playwright import api as reddit_api  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "data", "raw.jsonl")
BODY_CHARS = 1500

GITHUB_REPOS = [
    "mne-tools/mne-python",
    "brainflow-dev/brainflow",
    "OpenBCI/OpenBCI_GUI",
    "sccn/labstreaminglayer",
    "NeurodataWithoutBorders/pynwb",
    "NeuroTechX/moabb",
    "braindecode/braindecode",
    "sccn/eeglab",
    "SpikeInterface/spikeinterface",
    "timeflux/timeflux",
]
SUBREDDITS = ["BCI", "EEG", "OpenBCI", "neurotechnology", "compmathneuro"]
DISCOURSE = "https://mne.discourse.group"


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "bci-painpoints/0.1", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def github():
    token = os.environ.get("GH_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    for repo in GITHUB_REPOS:
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
                    "id": f"gh:{repo}#{i['number']}",
                    "source": f"github:{repo}",
                    "title": i["title"],
                    "body": (i.get("body") or "")[:BODY_CHARS],
                    "engagement": i["comments"] + i.get("reactions", {}).get("total_count", 0),
                    "url": i["html_url"],
                    "created": i["created_at"][:10],
                }


def reddit():
    for sub in SUBREDDITS:
        seen = set()
        for t in ("all", "year"):
            try:
                data = reddit_api("GET", f"/r/{sub}/top?t={t}&limit=100")
            except Exception as e:
                print(f"reddit {sub} {t}: {e}", file=sys.stderr)
                continue
            for c in data.get("data", {}).get("children", []):
                d = c["data"]
                if d["id"] in seen:
                    continue
                seen.add(d["id"])
                yield {
                    "id": f"rd:{d['id']}",
                    "source": f"reddit:r/{sub}",
                    "title": d["title"],
                    "body": (d.get("selftext") or "")[:BODY_CHARS],
                    "engagement": d["score"] + d["num_comments"],
                    "url": "https://www.reddit.com" + d["permalink"],
                    "created": time.strftime("%Y-%m-%d", time.gmtime(d["created_utc"])),
                }


def discourse(pages=8):
    seen = set()
    urls = [f"{DISCOURSE}/top.json?period=all"] + [f"{DISCOURSE}/latest.json?page={p}" for p in range(pages)]
    topics = []
    for url in urls:
        try:
            topics += get_json(url)["topic_list"]["topics"]
        except Exception as e:
            print(f"discourse {url}: {e}", file=sys.stderr)
    for t in topics:
        if t["id"] in seen:
            continue
        seen.add(t["id"])
        try:
            full = get_json(f"{DISCOURSE}/t/{t['id']}.json")
            body = re.sub(r"<[^>]+>", " ", full["post_stream"]["posts"][0]["cooked"])
        except Exception as e:
            print(f"discourse topic {t['id']}: {e}", file=sys.stderr)
            body = ""
        time.sleep(0.3)
        yield {
            "id": f"mne:{t['id']}",
            "source": "discourse:mne",
            "title": t["title"],
            "body": re.sub(r"\s+", " ", body)[:BODY_CHARS],
            "engagement": t.get("posts_count", 0) + t.get("like_count", 0),
            "url": f"{DISCOURSE}/t/{t['slug']}/{t['id']}",
            "created": t["created_at"][:10],
        }


def main():
    tmp = OUT + ".tmp"
    counts = {}
    with open(tmp, "w") as f:
        for gen in (github, reddit, discourse):
            for item in gen():
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                counts[gen.__name__] = counts.get(gen.__name__, 0) + 1
            print(f"{gen.__name__}: {counts.get(gen.__name__, 0)} items", file=sys.stderr)
    os.replace(tmp, OUT)


if __name__ == "__main__":
    main()
