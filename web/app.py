#!/usr/bin/env python3
"""
Paid idea-validation reports: pay once, get the phase-1 report.

Flow: landing form → Stripe Checkout → webhook (or success-page check) marks the
job paid → a single worker thread runs `phase1/validation_tool.py report` with the
Claude API (VALIDATION_LLM=api) → the report renders at /r/<token>. A failed run
is refunded automatically. The report link is also put in the Stripe receipt, so
no email service is needed.

Config (web/.env, loaded by systemd): STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
ANTHROPIC_API_KEY, BASE_URL, PRICE_USD, ADMIN_TOKEN, VALIDATION_LLM.
"""

import html
import json
import logging
import os
import secrets
import sqlite3
import subprocess
import threading
import time

import stripe
from flask import Flask, abort, redirect, request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "web", "jobs.db")
SAMPLE = os.path.join(ROOT, "web", "sample_report.json")
PYTHON = os.path.join(ROOT, ".venv", "bin", "python")
TOOL = os.path.join(ROOT, "phase1", "validation_tool.py")

BASE_URL = os.environ.get("BASE_URL", "https://validate.jvalansi.com").rstrip("/")
PRICE_USD = int(os.environ.get("PRICE_USD", "29"))
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
REPORT_TIMEOUT_S = 900
IDEA_MIN, IDEA_MAX = 10, 400

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("validate")
app = Flask(__name__)


# ── storage ───────────────────────────────────────────────────────────────────

def db():
    conn = sqlite3.connect(DB, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS jobs (
            token TEXT PRIMARY KEY, idea TEXT NOT NULL, status TEXT NOT NULL,
            stripe_session TEXT, payment_intent TEXT, report_json TEXT, error TEXT,
            created REAL NOT NULL, updated REAL NOT NULL)""")


def get_job(token):
    with db() as c:
        return c.execute("SELECT * FROM jobs WHERE token = ?", (token,)).fetchone()


def update_job(token, **fields):
    fields["updated"] = time.time()
    cols = ", ".join(f"{k} = ?" for k in fields)
    with db() as c:
        c.execute(f"UPDATE jobs SET {cols} WHERE token = ?", (*fields.values(), token))


def mark_paid(token, session):
    """Idempotent: only a pending job moves to paid."""
    with db() as c:
        c.execute("UPDATE jobs SET status = 'paid', payment_intent = ?, updated = ? "
                  "WHERE token = ? AND status = 'pending_payment'",
                  (session.get("payment_intent"), time.time(), token))


def llm_ready():
    return os.environ.get("VALIDATION_LLM") != "api" or bool(os.environ.get("ANTHROPIC_API_KEY"))


# ── worker ────────────────────────────────────────────────────────────────────

def run_report(idea):
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    out = subprocess.run([PYTHON, TOOL, "report", "--query", idea], capture_output=True, text=True,
                         timeout=REPORT_TIMEOUT_S, env=env, cwd=ROOT)
    start = out.stdout.find("\n{")
    text = out.stdout[start + 1:] if start != -1 else out.stdout
    report = json.loads(text)
    analysis = report.get("claude_analysis")
    if not analysis or "error" in analysis:
        raise RuntimeError(f"analysis failed: {(analysis or {}).get('error', 'no analysis')}")
    return report


def refund(job):
    if not job["payment_intent"]:
        return
    try:
        stripe.Refund.create(payment_intent=job["payment_intent"])
        log.info("refunded %s", job["token"])
    except Exception as e:
        log.error("REFUND FAILED for %s (%s): %s", job["token"], job["payment_intent"], e)


def worker():
    while True:
        with db() as c:
            job = c.execute("SELECT * FROM jobs WHERE status = 'paid' ORDER BY updated LIMIT 1").fetchone()
        if not job:
            time.sleep(3)
            continue
        token = job["token"]
        with db() as c:  # atomic claim, safe if a second worker ever runs
            if c.execute("UPDATE jobs SET status = 'running', updated = ? WHERE token = ? AND status = 'paid'",
                         (time.time(), token)).rowcount != 1:
                continue
        log.info("running %s: %s", token, job["idea"][:80])
        try:
            report = run_report(job["idea"])
            update_job(token, status="done", report_json=json.dumps(report))
            log.info("done %s", token)
        except Exception as e:
            log.exception("failed %s", token)
            update_job(token, status="failed", error=str(e)[:500])
            refund(job)


# ── pages ─────────────────────────────────────────────────────────────────────

CSS = """body{font-family:system-ui,-apple-system,sans-serif;max-width:760px;margin:0 auto;padding:32px 18px;
line-height:1.55;color:#1a202c}h1{font-size:2rem;line-height:1.2}h2{margin-top:2rem;font-size:1.2rem}
.card{border:1px solid #e2e8f0;border-radius:10px;padding:16px 18px;margin:14px 0}
textarea{width:100%;box-sizing:border-box;font:inherit;padding:10px;border:1px solid #cbd5e0;border-radius:8px}
button{background:#2563eb;color:#fff;border:0;border-radius:8px;padding:12px 20px;font-size:1rem;cursor:pointer}
.muted{color:#718096;font-size:.9rem}.pos{color:#15803d}.neg{color:#b91c1c}
.verdict{font-size:1.25rem;font-weight:700}.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px}
footer{margin-top:3rem;color:#a0aec0;font-size:.85rem}a{color:#2563eb}"""


def page(title, body, refresh=None):
    meta = f'<meta http-equiv="refresh" content="{refresh}">' if refresh else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">{meta}'
            f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}"
            f'<footer>Validation Tool · <a href="https://apps.jvalansi.com/privacy.html">Privacy</a> · '
            f'<a href="https://apps.jvalansi.com/terms.html">Terms</a> · '
            f"If a report fails to generate, you are refunded automatically.</footer></body></html>")


@app.get("/")
def index():
    closed = "" if llm_ready() else '<p class="neg">New orders are paused briefly — please check back soon.</p>'
    return page("Validate your startup idea in 10 minutes", f"""
<h1>Is anyone already paying for your idea?</h1>
<p>Describe your product idea. In about 10 minutes you get an evidence-based report: who already sells it
and what they raised, what competitors charge, whether people are asking for it on Reddit and Hacker News,
search-interest trends, regulatory red flags, and an order-of-magnitude revenue estimate with the key risks.</p>
<div class="card"><form method="post" action="/checkout">
<label for="idea"><b>Your idea</b> <span class="muted">(one or two sentences)</span></label>
<textarea id="idea" name="idea" rows="4" minlength="{IDEA_MIN}" maxlength="{IDEA_MAX}" required
placeholder="e.g. An app that answers building-code questions for small contractors"></textarea>
<p><button type="submit">Get my report — ${PRICE_USD}</button></p></form>{closed}
<p class="muted">One-time payment via Stripe. <a href="/sample">See a sample report</a>.</p></div>
<h2>What's checked</h2>
<ul><li>Operating competitors and their funding (not just Product Hunt launches)</li>
<li>Observed competitor prices and whether one customer can pay back acquisition costs</li>
<li>Demand signals from Reddit, Hacker News and Google Trends</li>
<li>Who owns the buyer-intent search results — is organic entry realistic?</li>
<li>Licensing or regulatory restrictions on selling it</li></ul>""")


@app.post("/checkout")
def checkout():
    idea = " ".join((request.form.get("idea") or "").split())
    if not (IDEA_MIN <= len(idea) <= IDEA_MAX):
        return page("Check your idea", f"<p>Please describe the idea in {IDEA_MIN}–{IDEA_MAX} characters.</p>"
                    '<p><a href="/">Back</a></p>'), 400
    if not llm_ready():
        return page("Paused", "<p>New orders are paused briefly — no payment was taken.</p>"), 503
    token = secrets.token_urlsafe(16)
    now = time.time()
    with db() as c:
        c.execute("INSERT INTO jobs (token, idea, status, created, updated) VALUES (?, ?, 'pending_payment', ?, ?)",
                  (token, idea, now, now))
    report_url = f"{BASE_URL}/r/{token}"
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"quantity": 1, "price_data": {
            "currency": "usd", "unit_amount": PRICE_USD * 100,
            "product_data": {"name": "Idea validation report"}}}],
        success_url=f"{report_url}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/",
        metadata={"token": token},
        payment_intent_data={"description": f"Idea validation report — view it at {report_url}",
                             "metadata": {"token": token}},
    )
    update_job(token, stripe_session=session.id)
    return redirect(session.url, code=303)


@app.post("/stripe/webhook")
def stripe_webhook():
    try:
        event = stripe.Webhook.construct_event(request.get_data(), request.headers.get("Stripe-Signature", ""),
                                               WEBHOOK_SECRET)
    except Exception:
        abort(400)
    if event["type"] == "checkout.session.completed":
        s = event["data"]["object"]
        token = (s.get("metadata") or {}).get("token")
        if token and s.get("payment_status") == "paid":
            mark_paid(token, s)
    return "", 200


@app.get("/r/<token>")
def report_page(token):
    job = get_job(token)
    if not job:
        abort(404)
    # Don't depend on webhook timing: the success redirect carries the session to verify.
    if job["status"] == "pending_payment" and request.args.get("session_id") == job["stripe_session"]:
        s = stripe.checkout.Session.retrieve(job["stripe_session"])
        if s.payment_status == "paid":
            mark_paid(token, s)
            job = get_job(token)
    idea = html.escape(job["idea"])
    if job["status"] == "done":
        return page(f"Report: {job['idea'][:60]}", render_report(json.loads(job["report_json"]), idea))
    if job["status"] == "failed":
        return page("Report failed", f"<h1>Sorry — this report failed</h1><p>“{idea}”</p>"
                    "<p>Your payment has been refunded automatically; it can take 5–10 days to appear.</p>")
    if job["status"] == "pending_payment":
        return page("Awaiting payment", f"<h1>Waiting for payment</h1><p>“{idea}”</p>"
                    '<p class="muted">If you completed checkout, this page updates within a minute.</p>', refresh=15)
    return page("Working on your report", f"<h1>Researching your idea…</h1><p>“{idea}”</p>"
                "<p>This takes about 5–15 minutes. Keep this page open or bookmark it — the link is also in "
                'your Stripe receipt.</p><p class="muted">This page refreshes automatically.</p>', refresh=20)


@app.get("/sample")
def sample():
    if not os.path.exists(SAMPLE):
        abort(404)
    rep = json.load(open(SAMPLE))
    return page("Sample report", '<p class="muted">Sample report</p>' + render_report(rep, html.escape(rep["query"])))


@app.post("/admin/run")
def admin_run():
    """Free run for testing: POST idea with ?token=ADMIN_TOKEN."""
    if not ADMIN_TOKEN or not secrets.compare_digest(request.args.get("token", ""), ADMIN_TOKEN):
        abort(403)
    idea = " ".join((request.form.get("idea") or "").split())[:IDEA_MAX]
    token = secrets.token_urlsafe(16)
    now = time.time()
    with db() as c:
        c.execute("INSERT INTO jobs (token, idea, status, created, updated) VALUES (?, ?, 'paid', ?, ?)",
                  (token, idea, now, now))
    return {"url": f"{BASE_URL}/r/{token}"}


# ── report rendering ──────────────────────────────────────────────────────────

def _items(values, cls=""):
    return "".join(f'<li class="{cls}">{html.escape(str(v))}</li>' for v in values or [])


def _links(posts, key="title"):
    out = []
    for p in posts or []:
        label = html.escape(str(p.get(key) or p.get("name") or p.get("url", "")))
        url = html.escape(p.get("url", ""), quote=True)
        out.append(f'<li><a href="{url}" rel="nofollow noopener" target="_blank">{label}</a></li>' if url
                   else f"<li>{label}</li>")
    return "".join(out) or '<li class="muted">None found</li>'


def _money(v):
    return f"${v:,.0f}" if isinstance(v, (int, float)) else "—"


def render_report(rep, idea):
    s, a, src = rep.get("summary", {}), rep.get("claude_analysis", {}), rep.get("sources", {})
    rev = rep.get("revenue_estimate", {})
    inc, tr = src.get("incumbents", {}), src.get("google_trends", {})
    prob = a.get("suggested_probability")
    funding = inc.get("max_funding_usd")
    return f"""<h1>{idea}</h1>
<div class="card"><div class="verdict">{html.escape(s.get("verdict", "—"))}</div>
<p>Competition: <b>{html.escape(str(s.get("competition", "—")))}</b>
{f" · largest raise seen: <b>{_money(funding)}</b>" if funding else ""}</p>
<div class="grid"><div><b>Strengths</b><ul>{_items(s.get("positive_signals"), "pos")}</ul></div>
<div><b>Concerns</b><ul>{_items(s.get("negative_signals"), "neg")}</ul></div></div></div>
<h2>Market and revenue</h2><div class="card">
<p>{html.escape(a.get("tam_assessment", ""))}</p>
<p>{html.escape(a.get("pricing_assessment", ""))}</p>
<div class="grid"><div>Potential customers: <b>~{a.get("tam_customers", 0):,}</b></div>
<div>Revenue per customer: <b>~{_money(a.get("price_per_customer_annual"))}/yr</b></div>
<div>Full market potential: <b>~{_money(a.get("value"))}/yr</b></div>
<div>Realistic capture: <b>{f"{prob:.0%}" if isinstance(prob, (int, float)) else "—"}</b></div></div>
<p class="muted">{html.escape(a.get("probability_reasoning", ""))}</p>
<p class="muted">Observed competitor price anchor: {_money(rev.get("price_anchor_usd"))}
({html.escape(str(rev.get("price_source", "")))})</p></div>
<h2>Risks and opportunities</h2><div class="grid">
<div class="card"><b>Key risks</b><ul>{_items(a.get("key_risks"), "neg")}</ul></div>
<div class="card"><b>Key opportunities</b><ul>{_items(a.get("key_opportunities"), "pos")}</ul></div></div>
<h2>Regulatory</h2><div class="card"><p><b>{html.escape(str(a.get("legal_status", "unknown")))}</b> —
{html.escape(a.get("legal_reasoning", ""))}</p></div>
<h2>Evidence</h2>
<div class="card"><b>Companies already selling</b> ({inc.get("operators_found", 0)} found)<ul>{_links(inc.get("operators"), "name")}</ul></div>
<div class="card"><b>Reddit discussions</b><ul>{_links(src.get("reddit", {}).get("top_posts"))}</ul></div>
<div class="card"><b>Hacker News</b> ({src.get("hacker_news", {}).get("total_results", 0)} posts)<ul>{_links(src.get("hacker_news", {}).get("top_posts"))}</ul></div>
<div class="card"><b>Product Hunt launches</b><ul>{_links(src.get("product_hunt", {}).get("top_products"), "name")}</ul></div>
<div class="card"><b>Search interest</b>: {html.escape(str(tr.get("average_interest", "no data")))} / 100,
trend {html.escape(str(tr.get("trend_direction", "—")))}</div>
<p class="muted">Figures are order-of-magnitude estimates from public web evidence, not financial advice.
Verify key competitors and prices before deciding.</p>"""


init_db()
threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8010)
