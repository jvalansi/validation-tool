#!/usr/bin/env python3
"""
Sweep every niche in niches/, rank all pain clusters together, and run the top ones
through phase1/validation_tool.py. Posts the result to Discord #validation-tool.

Steps per niche are cached (raw.jsonl, extracted.jsonl, taxonomy.json, assigned.json),
so a killed sweep resumes where it stopped. Delete data/<niche>/ to redo a niche.
Validation results are kept in validated.json, so each sweep validates the top N clusters
not validated before.

Usage: python sweep.py [--top N] [--niches a,b,c]
"""

import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
VT = os.path.join(HERE, "..")
PY = sys.executable
SWEEP = os.path.join(HERE, "reports", "SWEEP.md")
VALIDATED = os.path.join(HERE, "validated.json")


def load_validated():
    return json.load(open(VALIDATED)) if os.path.exists(VALIDATED) else {}


def save_validated(cache):
    with open(VALIDATED + ".tmp", "w") as f:
        json.dump(cache, f, indent=1, ensure_ascii=False)
    os.replace(VALIDATED + ".tmp", VALIDATED)


def run(cmd):
    print("$", " ".join(cmd), file=sys.stderr, flush=True)
    return subprocess.run(cmd, cwd=HERE).returncode == 0


def rank(clusters):
    """Rank by each cluster's share of its own niche's pains, so a niche with 10x more data
    (BCI: 1,356 items vs ~50 elsewhere) doesn't take every slot. Excluded clusters never rank."""
    totals = {}
    for c in clusters:
        totals[c["niche"]] = totals.get(c["niche"], 0) + c["items"]
    for c in clusters:
        share = c["items"] / totals[c["niche"]] if totals[c["niche"]] else 0
        c["score"] = round(100 * share * (1 + c["paying"] / c["items"]) * c["fit"], 1) if c["items"] else 0.0
    return sorted((c for c in clusters if not c.get("excluded") and c["items"] >= 3),
                  key=lambda c: (c["score"], c["paying"]), reverse=True)


def validate(idea):
    out = subprocess.run([PY, os.path.join(VT, "phase1", "validation_tool.py"), "report", "--query", idea],
                         capture_output=True, text=True, timeout=1200, cwd=VT)
    start = out.stdout.find("\n{")
    rep = json.loads(out.stdout[start + 1:] if start != -1 else out.stdout)
    a = rep.get("claude_analysis") or {}
    return {"verdict": rep["summary"]["verdict"], "competition": rep["summary"]["competition"],
            "probability": a.get("suggested_probability"), "value": a.get("value"),
            "risks": a.get("key_risks", [])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--niches")
    args = ap.parse_args()
    niches = args.niches.split(",") if args.niches else sorted(
        f[:-5] for f in os.listdir(os.path.join(HERE, "niches")) if f.endswith(".json"))

    for n in niches:
        if not os.path.exists(os.path.join(HERE, "data", n, "raw.jsonl")):
            run([PY, "fetch.py", n])
        run([PY, "analyze.py", n])

    clusters = []
    for n in niches:
        path = os.path.join(HERE, "data", n, "clusters.json")
        if os.path.exists(path):
            clusters += json.load(open(path))
    ranked = rank(clusters)

    cache = load_validated()
    results = []
    for c in [c for c in ranked if f"{c['niche']}:{c['cid']}" not in cache][:args.top]:
        try:
            v = validate(c["product_idea"])
        except Exception as e:
            results.append((c, {"verdict": f"validation failed: {e}"}))  # not cached, retried next sweep
            continue
        v.update(niche=c["niche"], name=c["name"], idea=c["product_idea"], pain=c["description"],
                 score=c["score"], date=time.strftime("%Y-%m-%d"))
        cache[f"{c['niche']}:{c['cid']}"] = v
        save_validated(cache)
        results.append((c, v))

    lines = ["# Opportunity sweep", "",
             f"{len(niches)} niches, {len(clusters)} clusters ({len(clusters) - len(ranked)} excluded by profile or under 3 items).",
             "Score = 100 × share of the niche's pains × (1 + paying share) × fit (clusters with ≥3 items); fit and clustering are Claude judgements.", "",
             f"## {len(results)} newly validated (top-ranked clusters not validated in earlier sweeps)", ""]
    for i, (c, v) in enumerate(results, 1):
        lines += [f"### {i}. {c['product_idea']}  ({c['niche']}, score {c['score']})",
                  f"- Pain: {c['description']}",
                  f"- Items {c['items']} · paying signals {c['paying']} · fit {c['fit']}",
                  f"- Validation: **{v.get('verdict')}** · competition {v.get('competition')} · "
                  f"capture {v.get('probability')} · market ~${v.get('value') or 0:,}/yr",
                  *[f"  - risk: {r}" for r in v.get("risks", [])],
                  *[f"  - {u}" for u in c["evidence"][:3]], ""]
    done = {id(c) for c, _ in results}
    rest = [c for c in ranked if f"{c['niche']}:{c['cid']}" not in cache and id(c) not in done]
    lines += ["## Next 20 not yet validated", ""] + [
        f"- {c['score']} · {c['niche']} · {c['product_idea']}" for c in rest[:20]]
    os.makedirs(os.path.dirname(SWEEP), exist_ok=True)
    with open(SWEEP + ".tmp", "w") as f:
        f.write("\n".join(lines) + "\n")
    os.replace(SWEEP + ".tmp", SWEEP)

    sys.path.insert(0, VT)
    from phase2.notify import post
    post("**Opportunity sweep done** — top ideas after validation:\n" + "\n".join(
        f"{i}. {c['product_idea']} ({c['niche']}) — {v.get('verdict')}" for i, (c, v) in enumerate(results, 1))
        + "\nFull report: https://github.com/jvalansi/validation-tool/blob/main/phase0/reports/SWEEP.md")


if __name__ == "__main__":
    main()
