"""Paid Stripe checkouts for a live product, for phase 2 runs that send ads to a built product instead of a landing page."""

import base64
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime

OWNER_EMAIL_PREFIX = "jvalansi"  # the owner's own test purchases aren't customers
ENV_FILE = os.path.join(os.path.dirname(__file__), "..", "web", ".env")  # Lobsteady and MVP Verdict share this Stripe account


def _stripe_key():
    key = os.environ.get("STRIPE_SECRET_KEY")
    if not key and os.path.exists(ENV_FILE):
        key = next((l.split("=", 1)[1].strip() for l in open(ENV_FILE) if l.startswith("STRIPE_SECRET_KEY=")), None)
    if not key:
        raise RuntimeError("STRIPE_SECRET_KEY not set")
    return key


def host(url):
    h = urllib.parse.urlparse(url if "//" in url else f"//{url}").hostname or ""
    return h[4:] if h.startswith("www.") else h


def paid_checkouts(product_url, since_iso):
    """Completed Checkout Sessions with money paid, by someone other than the owner, since since_iso and whose
    success_url is on product_url's host.
    One Stripe account serves several products, so the host tells them apart."""
    since = int(datetime.fromisoformat(since_iso).timestamp())
    auth = "Basic " + base64.b64encode(f"{_stripe_key()}:".encode()).decode()
    count, after = 0, None
    while True:
        q = {"created[gte]": since, "status": "complete", "limit": 100, **({"starting_after": after} if after else {})}
        req = urllib.request.Request("https://api.stripe.com/v1/checkout/sessions?" + urllib.parse.urlencode(q),
                                     headers={"Authorization": auth})
        with urllib.request.urlopen(req, timeout=30) as r:
            page = json.loads(r.read())
        count += sum(1 for s in page["data"] if s.get("payment_status") == "paid" and s.get("amount_total")
                     and host(s.get("success_url") or "") == host(product_url)
                     and not ((s.get("customer_details") or {}).get("email") or "").lower().startswith(OWNER_EMAIL_PREFIX))
        if not page.get("has_more"):
            return count
        after = page["data"][-1]["id"]
