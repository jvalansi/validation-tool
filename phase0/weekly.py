#!/usr/bin/env python3
"""
Weekly idea pipeline, run from run.sh by cron:

  1. Claude proposes new niches (subreddits checked to exist) → niches/<name>.json
  2. sweep.py mines every niche and phase-1 validates the top clusters not validated before
  3. The best passing ideas ("validate further", by market value × capture) not yet in Notion
     are added with notion_create.py --ai-generated
  4. The highest-ROI Notion ideas with no "Phase 2 Tested" date (and not status ❌) are
     launched through phase 2, then stamped with today's date

Usage: python weekly.py [--new-niches 2] [--top 10] [--add 2] [--launch 2] [--skip-sweep] [--dry-run]
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
    return added


def launch_phase2(k, dry_run):
    pages = notion(f"databases/{NOTION_DB}/query", {
        "filter": {"and": [
            {"property": "Phase 2 Tested", "date": {"is_empty": True}},
            {"property": "סטטוס", "status": {"does_not_equal": STATUS_DROPPED}},
            {"property": "ROI", "formula": {"number": {"is_not_empty": True}}},
        ]},
        "sorts": [{"property": "ROI", "direction": "descending"}],
        "page_size": k,
    }, method="POST")["results"]
    launched = []
    for p in pages:
        name = "".join(t["plain_text"] for t in p["properties"]["Project"]["title"])
        if dry_run:
            launched.append(f"{name} (dry run, ROI {p['properties']['ROI']['formula'].get('number')})")
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
    ap.add_argument("--new-niches", type=int, default=2)
    ap.add_argument("--top", type=int, default=10, help="clusters to phase-1 validate per sweep")
    ap.add_argument("--add", type=int, default=2, help="passing ideas to add to Notion")
    ap.add_argument("--launch", type=int, default=2, help="untested Notion ideas to launch in phase 2")
    ap.add_argument("--skip-sweep", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="no Notion writes, no phase-2 launches")
    args = ap.parse_args()

    niches = [] if args.skip_sweep else propose_niches(args.new_niches)
    if not args.skip_sweep:
        subprocess.run([PY, "sweep.py", "--top", str(args.top)], cwd=HERE)
    added = add_to_notion(args.add, args.dry_run)
    launched = launch_phase2(args.launch, args.dry_run)

    (print if args.dry_run else post)("**Weekly idea pipeline**\n"
         f"- New niches: {', '.join(niches) or 'none'}\n"
         f"- Added to Notion (AI Generated): {', '.join(added) or 'none passed phase 1'}\n"
         f"- Phase 2 launched: {', '.join(launched) or 'none'}")


if __name__ == "__main__":
    main()
