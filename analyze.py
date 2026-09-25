#!/usr/bin/env python3
"""
Turn data/raw.jsonl into a ranked pain-point report (report.md).

  1. extract  — Claude labels each item: is it a recurring pain a product/service could solve?
                Who has it, how severe, any sign of paying. Cached in data/extracted.jsonl.
  2. taxonomy — Claude proposes clusters from all pains, with an ML-fit rating each.
  3. assign   — Claude assigns every pain to a cluster.
  4. report   — rank clusters by score() and write report.md.

Usage: python analyze.py
"""

import json
import os
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw.jsonl")
EXTRACTED = os.path.join(HERE, "data", "extracted.jsonl")
TAXONOMY = os.path.join(HERE, "data", "taxonomy.json")
ASSIGNED = os.path.join(HERE, "data", "assigned.json")
REPORT = os.path.join(HERE, "report.md")
CLAUDE_PATH = os.environ.get("CLAUDE_PATH", "/home/ubuntu/.local/bin/claude")
BATCH = 30
WORKERS = 4

PROFILE = (
    "The builder is an ML engineer with neural-decoding experience (spiking-data latent models, "
    "transformers on NLB/FALCON benchmarks), limited to ~3 evening hours/day, who can run servers "
    "and write software but has no wet lab or hardware manufacturing."
)


def claude_json(prompt):
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    r = subprocess.run([CLAUDE_PATH, "-p", prompt, "--output-format", "json"],
                       input="", capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"claude rc={r.returncode}: {r.stderr[-300:]}")
    text = json.loads(r.stdout).get("result", "")
    start = min(i for i in (text.find("["), text.find("{")) if i != -1)
    end = max(text.rfind("]"), text.rfind("}")) + 1
    return json.loads(text[start:end])


def write_atomic(path, text):
    with open(path + ".tmp", "w") as f:
        f.write(text)
    os.replace(path + ".tmp", path)


def extract_batch(items):
    compact = [{"id": i["id"], "source": i["source"], "title": i["title"], "body": i["body"][:800]} for i in items]
    prompt = (
        "You are mining brain-computer-interface / neural-data communities for product pain points.\n"
        "For each item decide if it reveals a RECURRING pain in doing BCI/EEG/neural-data work that a "
        "product or paid service could solve (e.g. setup friction, data wrangling, signal quality, "
        "reproducibility, compute, hardware/software integration, missing tooling, expertise gaps). "
        "One-off bugs in a specific function, announcements, news, and hype are NOT pains.\n"
        "Return ONLY a JSON array, one object per item:\n"
        '  {"id": str, "is_pain": bool, "pain": str (one generalized sentence, empty if not a pain), '
        '"who": "hobbyist"|"student"|"academic_lab"|"startup"|"clinician"|"developer"|"unknown", '
        '"severity": 1|2|3, "pay_signal": str (quote showing money/time spent or willingness to pay, else "")}\n\n'
        f"Items:\n{json.dumps(compact, ensure_ascii=False)}"
    )
    return claude_json(prompt)


def extract(raw):
    done = {}
    if os.path.exists(EXTRACTED):
        for line in open(EXTRACTED):
            d = json.loads(line)
            done[d["id"]] = d
    todo = [r for r in raw if r["id"] not in done]
    batches = [todo[i:i + BATCH] for i in range(0, len(todo), BATCH)]
    print(f"extract: {len(done)} cached, {len(batches)} batches to run", file=sys.stderr)
    with open(EXTRACTED, "a") as f, ThreadPoolExecutor(WORKERS) as ex:
        for n, result in enumerate(ex.map(_safe_extract, batches), 1):
            for d in result:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
                done[d["id"]] = d
            f.flush()
            print(f"  batch {n}/{len(batches)}", file=sys.stderr)
    return done


def _safe_extract(batch):
    try:
        return extract_batch(batch)
    except Exception as e:
        print(f"  extract failed ({len(batch)} items): {e}", file=sys.stderr)
        return []


def taxonomy(pains):
    lines = "\n".join(f"- [{p['who']}] {p['pain']}" for p in pains)
    prompt = (
        f"Below are {len(pains)} pain points mined from BCI/EEG/neural-data communities.\n"
        "Group them into 15-25 distinct clusters that each could be addressed by one product or service.\n"
        f"Builder profile: {PROFILE}\n"
        "Return ONLY a JSON array of objects: "
        '{"cid": short_snake_case, "name": str, "description": str, '
        '"ml_fit": float 0-1 (how well the builder profile can solve it), "fit_reason": str, '
        '"product_idea": str (one line)}\n\n' + lines
    )
    return claude_json(prompt)


def assign(pains, clusters):
    defs = json.dumps([{"cid": c["cid"], "description": c["description"]} for c in clusters])
    out = {}
    batches = [pains[i:i + 100] for i in range(0, len(pains), 100)]

    def run(batch):
        prompt = (
            f"Clusters:\n{defs}\n\nAssign each pain to the single best cid (or \"other\").\n"
            'Return ONLY a JSON object {"<id>": "<cid>", ...}.\n\n'
            + json.dumps([{"id": p["id"], "pain": p["pain"]} for p in batch], ensure_ascii=False)
        )
        try:
            return claude_json(prompt)
        except Exception as e:
            print(f"  assign failed: {e}", file=sys.stderr)
            return {}

    with ThreadPoolExecutor(WORKERS) as ex:
        for r in ex.map(run, batches):
            out.update(r)
    return out


def score(n, n_pay, ml_fit):
    """Rank = frequency × (1 + share of items with a paying signal) × ML fit."""
    if n == 0:
        return 0.0
    return round(n * (1 + n_pay / n) * ml_fit, 2)


def report(raw, pains, clusters, assigned):
    by_id = {r["id"]: r for r in raw}
    rows = []
    for c in clusters:
        members = [p for p in pains if assigned.get(p["id"]) == c["cid"]]
        pay = [p for p in members if p.get("pay_signal")]
        rows.append((score(len(members), len(pay), c["ml_fit"]), c, members, pay))
    rows.sort(key=lambda r: r[0], reverse=True)

    src = Counter(r["source"].split(":")[0] for r in raw)
    out = [
        "# BCI pain points — ranked",
        "",
        f"Items scanned: {len(raw)} ({', '.join(f'{k} {v}' for k, v in src.items())}); "
        f"labelled as pains: {len(pains)}.",
        "Score = count × (1 + share with paying signal) × ML fit. ML fit and clustering are Claude judgements, not measurements.",
        "",
    ]
    for rank, (s, c, members, pay) in enumerate(rows, 1):
        who = Counter(p["who"] for p in members).most_common(3)
        eng = sum(by_id[p["id"]]["engagement"] for p in members if p["id"] in by_id)
        out += [
            f"## {rank}. {c['name']} — score {s}",
            f"- {c['description']}",
            f"- Items: {len(members)} · paying signals: {len(pay)} · engagement: {eng} · who: "
            + ", ".join(f"{w} {n}" for w, n in who),
            f"- ML fit {c['ml_fit']}: {c['fit_reason']}",
            f"- Product idea: {c['product_idea']}",
            "- Evidence:",
        ]
        top = sorted(members, key=lambda p: (bool(p.get("pay_signal")), by_id.get(p["id"], {}).get("engagement", 0)), reverse=True)[:5]
        for p in top:
            r = by_id.get(p["id"], {})
            q = f' — "{p["pay_signal"]}"' if p.get("pay_signal") else ""
            out.append(f"  - [{r.get('title', p['id'])}]({r.get('url', '')}) ({r.get('source', '')}, {r.get('created', '')}){q}")
        out.append("")
    write_atomic(REPORT, "\n".join(out))


def main():
    raw = [json.loads(line) for line in open(RAW)]
    extracted = extract(raw)
    pains = [d for d in extracted.values() if d.get("is_pain") and d.get("pain")]
    print(f"pains: {len(pains)} / {len(extracted)}", file=sys.stderr)

    if not os.path.exists(TAXONOMY):
        write_atomic(TAXONOMY, json.dumps(taxonomy(pains), indent=1, ensure_ascii=False))
    clusters = json.load(open(TAXONOMY))
    if not os.path.exists(ASSIGNED):
        write_atomic(ASSIGNED, json.dumps(assign(pains, clusters), indent=1))
    assigned = json.load(open(ASSIGNED))

    report(raw, pains, clusters, assigned)
    print(f"wrote {REPORT}", file=sys.stderr)


if __name__ == "__main__":
    main()
