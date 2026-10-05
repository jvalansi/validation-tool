#!/usr/bin/env python3
"""
Weekly idea pipeline, run from run.sh by cron in two steps so the user can approve spend.

Sunday (default):

  1. Claude proposes new niches (subreddits checked to exist) → niches/<name>.json
  2. sweep.py mines every niche and phase-1 validates the top clusters not validated before
  3. The best passing ideas ("validate further", by market value × capture) not yet in Notion
     are added with notion_create.py --ai-generated, with a Claude-estimated Fun Score
     (Fun Estimated ticked) learned from the user's own scores
  4. Proposes the highest-ROI untested ideas (ROI ≥ MIN_ROI, not status ❌) for phase 2, posting
     them to Discord; the user ticks "Phase 2 Approved" in Notion. Market Signal isn't used: phase 2
     is what measures demand, and the signal double-counts competition already in ROI

Monday (--launch):
  5. Launches phase 2 for every approved idea with no "Phase 2 Tested" date, then stamps it

Usage: python weekly.py [--new-niches 2] [--top 10] [--add 2] [--propose 2] [--skip-sweep] [--dry-run]
       python weekly.py --launch [--dry-run]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

from analyze import PROFILE, claude_json
from sweep import HERE, VT, load_validated, save_validated
from fetch import RDT

PY = sys.executable
PHASE2_PY = "/home/ubuntu/miniconda3/bin/python"  # same interpreter as the phase-2 monitor cron
NOTION_DB = "17731083-1fdd-4c06-a3c3-c87aa758703a"
STATUS_DROPPED = "❌"
MIN_ROI = 1  # Notion ROI < 1: expected value is below the cost of the work weeks
JOURNAL = "/home/ubuntu/journal/journal-summary.md"

sys.path.insert(0, VT)
from phase2.notify import post  # noqa: E402


def notion(path, data=None, method="GET"):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}", method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization": f"Bearer {os.environ['NOTION_TOKEN']}", "Notion-Version": "2022-06-28",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def subreddit_exists(name):
    out = subprocess.run([RDT, "sub-info", name, "--json"], capture_output=True, text=True, timeout=60)
    try:
        return bool(json.loads(out.stdout)["data"].get("display_name"))
    except Exception:
        return False


def propose_niches(n):
    existing = {f[:-5]: json.load(open(os.path.join(HERE, "niches", f))).get("audience", "")
                for f in os.listdir(os.path.join(HERE, "niches")) if f.endswith(".json")}
    prompt = (
        f"We mine Reddit for recurring work pain points that a solo builder could turn into a product.\n"
        f"Builder profile: {PROFILE}\n"
        f"Niches already covered: {json.dumps(existing)}\n"
        f"Propose {n + 2} NEW niches: groups of people who pay for tools for their work, active on Reddit, "
        "and not overlapping the covered ones. Return ONLY a JSON array of "
        '{"name": short-kebab-case, "audience": str, "subreddits": [4-6 subreddit names without r/]}'
    )
    added = []
    for p in claude_json(prompt):
        name = re.sub(r"[^a-z0-9-]", "", p.get("name", "").lower())
        if len(added) == n or not name or name in existing:
            continue
        subs = [s for s in p.get("subreddits", []) if subreddit_exists(s)]
        if len(subs) < 2:
            print(f"skip niche {name}: only {subs} exist", file=sys.stderr)
            continue
        path = os.path.join(HERE, "niches", f"{name}.json")
        with open(path + ".tmp", "w") as f:
            json.dump({"audience": p["audience"], "subreddits": subs}, f, indent=1)
        os.replace(path + ".tmp", path)
        added.append(name)
    return added


def estimate_fun(ideas):
    """{page_id: fun} for [(page_id, name, description)], from the user's own Fun Scores.
    Tested 2026-10-02 against held-out scores: rank correlation 0.44, so it orders ideas
    reasonably but misses individual scores by ~0.09; ROI's 2/(2-fun) keeps that to ~8%."""
    scored, cur = [], None
    while True:
        d = notion(f"databases/{NOTION_DB}/query", {"page_size": 100, **({"start_cursor": cur} if cur else {}),
                   "filter": {"and": [{"property": "Fun Score", "number": {"is_not_empty": True}},
                                      {"property": "Fun Estimated", "checkbox": {"equals": False}}]}}, method="POST")
        for p in d["results"]:
            pr = p["properties"]
            scored.append(f"- {''.join(t['plain_text'] for t in pr['Project']['title'])}: "
                          f"{''.join(t['plain_text'] for t in pr['Description']['rich_text'])[:300]} → {pr['Fun Score']['number']}")
        if not d["has_more"]:
            break
        cur = d["next_cursor"]
    journal = open(JOURNAL).read() if os.path.exists(JOURNAL) else ""
    prompt = (
        "Predict the Fun Score the person below would give each new project idea, on their own 0-1 scale.\n"
        "They score two things and weigh them equally: (1) how fun or interesting it is while doing it, and "
        "(2) how educational or beneficial it is afterwards (skills learned, personal use, value to them). "
        "An idea outside their interests can still score well on (2). Rate both parts, then average them.\n"
        f"About the person (summary of their journal):\n{journal}\n\nTheir own fun scores:\n" + "\n".join(scored) +
        "\n\nNew ideas:\n" + "\n".join(f"- id {i}: {n}: {desc}" for i, n, desc in ideas) +
        '\n\nReturn ONLY a JSON object {"<id>": averaged score, ...}, using the same scale and spread they use.'
    )
    out = claude_json(prompt)
    return {i: min(max(float(out[i]), 0.0), 1.0) for i, _, _ in ideas if i in out}


def add_to_notion(k, dry_run):
    cache = load_validated()
    passing = sorted((key for key, v in cache.items()
                      if str(v.get("verdict", "")).startswith("validate further") and not v.get("page_id")),
                     key=lambda key: (cache[key].get("value") or 0) * (cache[key].get("probability") or 0),
                     reverse=True)
    added = []
    for key in passing[:k]:
        v = cache[key]
        if dry_run:
            added.append(f"{v['name']} (dry run)")
            continue
        out = subprocess.run([PY, os.path.join(VT, "phase1", "notion_create.py"), "--name", v["name"],
                              "--idea", f"{v['idea']} Pain: {v['pain']}", "--ai-generated"],
                             capture_output=True, text=True, timeout=1800, cwd=VT)
        m = re.search(r"^PAGE_ID=(\S+)", out.stdout, re.M)
        if not m:
            print(f"notion_create failed for {key}: {out.stderr[-500:]}", file=sys.stderr)
            continue
        v["page_id"] = m.group(1)
        save_validated(cache)
        added.append(v["name"])
    new = [(cache[key]["page_id"], cache[key]["name"], cache[key]["idea"])
           for key in passing[:k] if cache[key].get("page_id") and not cache[key].get("fun")]
    if new:
        try:
            for page_id, fun in estimate_fun(new).items():
                notion(f"pages/{page_id}", {"properties": {"Fun Score": {"number": round(fun, 2)},
                                                           "Fun Estimated": {"checkbox": True}}}, method="PATCH")
                next(cache[key] for key in passing[:k] if cache[key].get("page_id") == page_id)["fun"] = fun
            save_validated(cache)
        except Exception as e:
            print(f"fun estimate failed: {e}", file=sys.stderr)  # pages stay unscored (ROI ×1) for the user
    return added


UNTESTED = [{"property": "Phase 2 Tested", "date": {"is_empty": True}},
            {"property": "סטטוס", "status": {"does_not_equal": STATUS_DROPPED}}]


def page_name(p):
    return "".join(t["plain_text"] for t in p["properties"]["Project"]["title"])


def propose_phase2(k):
    pages = notion(f"databases/{NOTION_DB}/query", {
        "filter": {"and": UNTESTED + [
            {"property": "Phase 2 Approved", "checkbox": {"equals": False}},
            {"property": "ROI", "formula": {"number": {"greater_than_or_equal_to": MIN_ROI}}},
        ]},
        "sorts": [{"property": "ROI", "direction": "descending"}],
        "page_size": k,
    }, method="POST")["results"]
    return [f"{page_name(p)} (ROI {round(p['properties']['ROI']['formula'].get('number') or 0, 1)}) {p['url']}"
            for p in pages]


def launch_approved(dry_run):
    pages = notion(f"databases/{NOTION_DB}/query", {
        "filter": {"and": UNTESTED + [{"property": "Phase 2 Approved", "checkbox": {"equals": True}}]},
    }, method="POST")["results"]
    launched = []
    for p in pages:
        name = page_name(p)
        if dry_run:
            launched.append(f"{name} (dry run)")
            continue
        out = subprocess.run([PHASE2_PY, "-m", "phase2.cli", p["id"]], capture_output=True, text=True,
                             timeout=3600, cwd=VT, env=os.environ)
        if out.returncode != 0:
            post(f"**Phase 2 launch failed** for {name}:\n```{(out.stderr or out.stdout)[-1500:]}```")
            continue
        notion(f"pages/{p['id']}", {"properties": {"Phase 2 Tested": {"date": {"start": time.strftime("%Y-%m-%d")}}}},
               method="PATCH")
        launched.append(name)
    return launched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--launch", action="store_true", help="Monday step: launch approved ideas only")
    ap.add_argument("--new-niches", type=int, default=2)
    ap.add_argument("--top", type=int, default=10, help="clusters to phase-1 validate per sweep")
    ap.add_argument("--add", type=int, default=2, help="passing ideas to add to Notion")
    ap.add_argument("--propose", type=int, default=2, help="untested Notion ideas to propose for phase 2")
    ap.add_argument("--skip-sweep", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="no Notion writes, no phase-2 launches")
    args = ap.parse_args()
    say = print if args.dry_run else post

    if args.launch:
        launched = launch_approved(args.dry_run)
        say(f"**Phase 2 launched:** {', '.join(launched) or 'nothing approved'}")
        return

    niches = [] if args.skip_sweep else propose_niches(args.new_niches)
    if not args.skip_sweep:
        subprocess.run([PY, "sweep.py", "--top", str(args.top)], cwd=HERE)
    added = add_to_notion(args.add, args.dry_run)
    proposed = propose_phase2(args.propose)

    say("**Weekly idea pipeline**\n"
        f"- New niches: {', '.join(niches) or 'none'}\n"
        f"- Added to Notion (AI Generated): {', '.join(added) or 'none passed phase 1'}\n"
        "- Proposed for phase 2 (~$100 of ads each). Tick **Phase 2 Approved** in Notion by Monday 06:00 UTC "
        "to launch:\n" + "\n".join(f"  - {p}" for p in proposed or ["none qualify"]))


if __name__ == "__main__":
    main()
