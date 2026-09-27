"""Runnable check for the web app's state machine and rendering. No network, no payments.

    .venv/bin/python web/test_app.py
"""
import json, os, sys, tempfile
os.environ.setdefault("VALIDATION_LLM", "cli")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as web

web.DB = os.path.join(tempfile.mkdtemp(), "jobs.db")
web.init_db()
with web.db() as c:
    c.execute("INSERT INTO jobs (token, idea, status, created, updated) VALUES ('t1', 'idea', 'pending_payment', 0, 0)")

# Paying moves pending -> paid once; a replayed webhook never resets a running/done job.
web.mark_paid("t1", {"payment_intent": "pi_1"})
assert web.get_job("t1")["status"] == "paid"
web.update_job("t1", status="done")
web.mark_paid("t1", {"payment_intent": "pi_2"})
job = web.get_job("t1")
assert job["status"] == "done" and job["payment_intent"] == "pi_1", dict(job)

# The sample report renders and escapes user text.
rep = json.load(open(os.path.join(os.path.dirname(__file__), "sample_report.json")))
out = web.render_report(rep, web.html.escape("<script>x</script>"))
assert "&lt;script&gt;" in out and "<script>" not in out
assert "Companies already selling" in out
print("ok")
