#!/usr/bin/env python3
"""
Re-run phase 1 on every Notion idea (not ❌, with a Validation Query) not validated since --since.
Resumable: notion_validate stamps "Validated" only on success, so re-running with the same --since
picks up where a run stopped. Stops when Brave refuses a search (credit used up) instead of
mixing in ddgs results, which vary run to run.

Usage: python phase1/revalidate_all.py --since 2026-10-07T00:00:00Z [--workers 4]
"""

import argparse
import json
import os
import subprocess
import sys
import threading
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from notion_validate import EXIT_SEARCH_REFUSED, NOTION_TOKEN, NOTION_VERSION, PYTHON  # noqa: E402

DB = "17731083-1fdd-4c06-a3c3-c87aa758703a"


def todo(since):
    pages, cur = [], None
    while True:
        req = urllib.request.Request(f"https://api.notion.com/v1/databases/{DB}/query", method="POST", data=json.dumps({
            "page_size": 100, **({"start_cursor": cur} if cur else {}),
            "filter": {"and": [{"property": "סטטוס", "status": {"does_not_equal": "❌"}},
                               {"property": "Validation Query", "rich_text": {"is_not_empty": True}},
                               {"or": [{"property": "Validated", "date": {"is_empty": True}},
                                       {"property": "Validated", "date": {"before": since}}]}]}}).encode(),
            headers={"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": NOTION_VERSION, "Content-Type": "application/json"})
        d = json.load(urllib.request.urlopen(req, timeout=30))
        pages += [(p["id"], "".join(t["plain_text"] for t in p["properties"]["Project"]["title"])) for p in d["results"]]
        if not d["has_more"]:
            return pages
        cur = d["next_cursor"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True, help="ISO time; ideas validated after it are skipped")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    pages = todo(args.since)
    print(f"validating {len(pages)}", flush=True)
    refused, failed = threading.Event(), []

    def one(item):
        i, (pid, name) = item
        if refused.is_set():
            return
        try:
            out = subprocess.run([PYTHON, os.path.join(HERE, "notion_validate.py"), pid, "--skip-trends", "--require-brave"],
                                 capture_output=True, text=True, timeout=900)
            code, err = out.returncode, out.stderr[-300:]
        except subprocess.TimeoutExpired:
            code, err = -1, "timeout"
        if code == EXIT_SEARCH_REFUSED:
            refused.set()
        elif code:
            failed.append(name)
        print(f"[{i}/{len(pages)}] {'ok' if code == 0 else 'REFUSED' if code == EXIT_SEARCH_REFUSED else 'FAILED'} {name[:60]}"
              + ("" if code == 0 else f": {err}"), flush=True)

    with ThreadPoolExecutor(args.workers) as ex:
        list(ex.map(one, enumerate(pages, 1)))
    left = len(todo(args.since))
    print(f"DONE. failed: {failed}. {'Brave refused (top up credit), ' if refused.is_set() else ''}"
          f"{left} left; re-run with --since {args.since} to resume.", flush=True)
    sys.exit(EXIT_SEARCH_REFUSED if refused.is_set() else 1 if failed else 0)


if __name__ == "__main__":
    main()
