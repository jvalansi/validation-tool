#!/usr/bin/env python3
"""
MVP builds for next week's phase-2 ideas, run by weekly.py on Sunday after this week's proposals.

The k highest-ROI untested ideas after this week's proposals, with no Product URL and no "MVP Build" note, each get
a headless Claude Code agent that builds and deploys a paid web app at <slug>.javolabs.com (same stack as legal-qa
and deepestate). Built and answering over HTTPS → Product URL is set, so next week phase 2 sends the ads to the app
instead of a landing page. The outcome goes in the "MVP Build" property either way (clear it to retry), including
any paid API the app needs that the user has to sign up for.

Usage: python build_mvp.py [--k 2] [--skip <page-id> ...] [--page <page-id> [--no-write]] [--dry-run]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import time
import urllib.request

from weekly import MIN_ROI, NOTION_DB, UNTESTED, VT, notion, page_name, post

BUILD_TIMEOUT = 4 * 3600
STATUSES = ("built", "skipped", "blocked", "failed")

PROMPT = """Build and deploy a working MVP web app on this server (Ubuntu, /home/ubuntu) for the idea "{name}" (Notion
page {page_id} in the validation-tool ideas DB). Next week it gets a Google Ads test that sends paid clicks straight
to it and counts paid Stripe checkouts, so it must be live, work end to end, and take payment. Nobody is around to
answer questions: decide yourself and report your decisions.

The idea (from the Notion row):
- Description: {description}
- Pain/desire: {pain}
- Customer group: {customers}
- Price: about ${price}/yr per customer
- Competitors: {competitors}
- Reviewer's note: {review}

The product spec - the owner's decisions. Build exactly this: its customer, market and language, its input and output,
its scenarios (the first is the MVP), and nothing it lists as out of scope:
{spec}

First decide whether this can be delivered as a web service that does the job for a visitor right away (an answer,
a report, a generated file, a tool they use). If it can't (hardware, a two-sided marketplace that needs supply first,
licensed or regulated work, anything needing manual labour per customer), build nothing and report "skipped". If it
can only work with a paid API or data source you can't sign up for, build it on free sources if the result is still
useful, and list that API under "needs"; if it can't work at all without it, report "blocked" with the API under
"needs". Never invent numbers or data: every figure the app shows comes from a cited source or is computed in code.

The product:
- Give ad visitors the real thing for free a few times (2-3 uses per browser), then a Stripe Checkout paywall. Price
  it from the yearly price above, as a monthly subscription unless a one-time purchase clearly fits better.
- Keep it minimal and mobile-friendly: a landing section saying what it does above the tool itself, the result page,
  the paywall, privacy and terms pages. No account system beyond the email Stripe gives you.
- Load the frontend-design skill (Skill tool, skill "frontend-design") and give it a distinctive, intentional look.

Implementation (follow existing conventions; read these first):
- Reference apps: /home/ubuntu/legal-qa and /home/ubuntu/deepestate (Flask + gunicorn + systemd + nginx + Stripe
  Checkout + webhook + free-use quota), and /home/ubuntu/validation-tool/web/app.py. Reuse their patterns.
- Pick a short lowercase slug for the product. /home/ubuntu/<slug> must not exist yet and the GitHub repo
  jvalansi/<slug> must not exist yet (check with `gh repo view`); pick another slug if either is taken.
- Stripe: the shared live account key is STRIPE_SECRET_KEY in /home/ubuntu/validation-tool/web/.env. Create a new
  Product + Price via the API and a new webhook endpoint for this app (its secret in this app's own .env). Checkout
  success_url must be on this app's own host (phase 2 counts sales by success_url host). Stripe objects in the
  installed SDK are not dicts: call .to_dict() before .get().
- LLM, if the product needs one: Anthropic API, key ANTHROPIC_API_KEY in /home/ubuntu/validation-tool/web/.env,
  model claude-sonnet-5. Load the claude-api skill (Skill tool, skill "claude-api") before writing the API code.
- Host at https://<slug>.javolabs.com: add a Route 53 A record to this server's public IP (no wildcard exists; load AWS
  keys with `set -a; source <(grep -E '^AWS_' /home/ubuntu/.env); set +a`; the zone is javolabs.com), nginx site +
  certbot TLS like the other sites, systemd unit with EnvironmentFile (no inline secrets), gunicorn on an unused
  127.0.0.1 port (check with `ss -ltn`; 8010-8060 are taken). Use `systemctl restart`, never stop+start.
- Code in /home/ubuntu/<slug>, pushed to a new private GitHub repo jvalansi/<slug>. gh auth:
  `export $(cat /home/ubuntu/.env | xargs)`; push with
  `GH=$(grep -oP 'GH_TOKEN=\\K\\S+' /home/ubuntu/.env); git push https://$GH@github.com/jvalansi/<slug>.git main`.
  Never commit .env, databases or secrets. End commit messages with:
  Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
- Leave one small runnable test (test_app.py) covering the free-quota logic and the product's core computation.
- After deploying, copy the nginx site and systemd unit into /home/ubuntu/server-config (see its README), then
  pull --rebase, commit and push that repo.
- Verify end to end: the site loads over HTTPS, a real example input gets a real result, Stripe Checkout opens, and a
  webhook test event is accepted. Do not make a real payment. Delete your test results from the app's database.

End your reply with exactly one JSON object and nothing after it:
{{"status": "built" | "skipped" | "blocked" | "failed", "url": "https://<slug>.javolabs.com" or null,
"repo": "jvalansi/<slug>" or null, "needs": ["<paid API>: <what it adds, its price>", ...],
"note": "<one line: what the app does, or why it was skipped/blocked/failed>"}}"""

BLIND = """

This is a blind rebuild, to compare with an app already built for this idea: build a new app under a new slug as if
none existed. Don't read, use or change any existing app for this idea, its Notion Product URL, or its repo."""


def text(p, name):
    prop = p["properties"].get(name) or {}
    return "".join(t["plain_text"] for t in prop.get(prop.get("type"), []) or []) if prop else ""


def candidates(k, skip=()):
    """Next week's proposals: the top untested ideas by ROI, minus this week's, with no app and no build attempt."""
    pages = notion(f"databases/{NOTION_DB}/query", {
        "filter": {"and": UNTESTED + [
            {"property": "Phase 2 Approved", "checkbox": {"equals": False}},
            {"property": "ROI", "formula": {"number": {"greater_than_or_equal_to": MIN_ROI}}},
            {"property": "Product URL", "url": {"is_empty": True}},
            {"property": "MVP Build", "rich_text": {"is_empty": True}},
        ]},
        "sorts": [{"property": "ROI", "direction": "descending"}],
        "page_size": k + len(skip),
    }, method="POST")["results"]
    return [p for p in pages if p["id"] not in skip][:k]


def prompt_for(p):
    props = p["properties"]
    try:
        competitors = ", ".join(c["name"] for c in json.loads(text(p, "Competitors") or "[]")) or "none recorded"
    except ValueError:
        competitors = "none recorded"
    return PROMPT.format(name=page_name(p), page_id=p["id"], description=text(p, "Description") or "-",
                         pain=text(p, "Pain/Desire") or "-", customers=text(p, "Customer Group") or "-",
                         price=props["Price/Customer/yr ($)"]["number"] or "unknown", competitors=competitors,
                         review=text(p, "Review Note") or "-", spec=product_spec(p["id"]))


def product_spec(page_id):
    """The idea's Notion spec, written first if it has none (open questions take their defaults)."""
    import sys
    sys.path.insert(0, os.path.join(VT, "phase1"))
    from spec import spec
    return spec(page_id)


def parse_result(reply):
    """The agent's closing JSON object -> a dict with a known status; failed if it's missing or malformed."""
    try:
        start = [m.start() for m in re.finditer(r'\{\s*"status"', reply)][-1]
        r = json.loads(reply[start:reply.rfind("}") + 1])
    except (IndexError, ValueError):
        return {"status": "failed", "url": None, "needs": [], "note": "no result JSON: " + reply[-300:]}
    if r.get("status") not in STATUSES:
        r["status"] = "failed"
    r.setdefault("needs", [])
    return r


def live(url, tries=20):
    """200 over HTTPS; retried for a while because this server's resolver caches the name's NXDOMAIN (up to the
    zone's 900s negative TTL) if it was looked up before the agent created the record."""
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                        timeout=30) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(60 if i < tries - 1 else 0)
    return False


def summary(r):
    """One line for the MVP Build property and the Discord report."""
    s = f"{time.strftime('%Y-%m-%d')} {r['status']}: {r.get('note') or ''}"
    if r.get("needs"):
        s += " | needs: " + "; ".join(r["needs"])
    return s[:2000]


def build(p, write=True):
    claude = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}  # the CLI runs on the subscription
    try:
        out = subprocess.run([claude, "-p", prompt_for(p) + ("" if write else BLIND), "--output-format", "json", "--model", "claude-opus-5-5",
                              "--dangerously-skip-permissions"],
                             capture_output=True, text=True, timeout=BUILD_TIMEOUT, env=env, cwd="/home/ubuntu")
        r = parse_result(json.loads(out.stdout).get("result", ""))
    except subprocess.TimeoutExpired:
        r = {"status": "failed", "url": None, "needs": [], "note": f"timed out after {BUILD_TIMEOUT // 3600}h"}
    except ValueError:
        r = {"status": "failed", "url": None, "needs": [], "note": "CLI error: " + (out.stderr or out.stdout)[-300:]}
    if r["status"] == "built" and not (r.get("url") and live(r["url"])):
        r.update(status="failed", note=f"reported built but {r.get('url')} isn't answering; {r.get('note')}")
    if not write:
        return r
    props = {"MVP Build": {"rich_text": [{"text": {"content": summary(r)}}]}}
    if r["status"] == "built":
        props["Product URL"] = {"url": r["url"]}
    notion(f"pages/{p['id']}", {"properties": props}, method="PATCH")
    return r


def run(k, skip=(), dry_run=False):
    """Builds one idea at a time (they'd race for ports and server-config) and posts the outcomes."""
    pages = candidates(k, skip)
    if dry_run:
        print("Would build: " + (", ".join(page_name(p) for p in pages) or "nothing"))
        return
    lines = []
    for p in pages:
        r = build(p)
        lines.append(f"- {page_name(p)}: {r.get('url') or ''} {summary(r)} {p['url']}")
    if lines:
        post("**MVP builds for next week's phase 2** (built ones get ads to the app; add any API listed under "
             "needs if it's worth it, or clear MVP Build in Notion to retry):\n" + "\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=2)
    ap.add_argument("--skip", nargs="*", default=[], help="page ids not to build (this week's proposals)")
    ap.add_argument("--page", help="build this page only")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-write", action="store_true", help="with --page: blind rebuild under a new slug, Notion left as is (to compare)")
    args = ap.parse_args()
    if args.page:
        r = build(notion(f"pages/{args.page}"), write=not args.no_write)
        print(json.dumps(r, indent=2))
        return
    run(args.k, args.skip, args.dry_run)


if __name__ == "__main__":
    main()
