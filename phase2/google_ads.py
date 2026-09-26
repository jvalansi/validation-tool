"""
Launch and cap Google Ads Search campaigns via the Google Ads REST API.

Access is granted to the Google Cloud project behind the OAuth client (the
developer token became optional on 2026-09-09). Needs, in the environment:

  GOOGLE_ADS_CUSTOMER_ID      ads account, digits only
  GOOGLE_ADS_CLIENT_ID        OAuth client of the approved Cloud project
  GOOGLE_ADS_CLIENT_SECRET
  GOOGLE_ADS_REFRESH_TOKEN    scope https://www.googleapis.com/auth/adwords
  GOOGLE_ADS_LOGIN_CUSTOMER_ID  optional, if accessed through a manager account
  GOOGLE_ADS_API_VERSION      optional, default v25

Campaigns are created PAUSED and enabled only after every part succeeds, so a
failed launch never leaves a half-built campaign spending. The hard cap is
enforced by enforce_caps(), run from the daily monitor.
"""

import json
import os
import urllib.parse
import urllib.request
from datetime import date

API_VERSION = os.environ.get("GOOGLE_ADS_API_VERSION", "v25")
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "ads_campaigns.json")

# geoTargetConstants: US, UK, Canada, Australia; languageConstants: English
GEO_TARGETS = [2840, 2826, 2124, 2036]
LANGUAGE_ENGLISH = 1000
# Google may spend up to 2x the daily budget on any one day.
OVERDELIVERY = 2


def configured():
    return all(os.environ.get(k) for k in (
        "GOOGLE_ADS_CUSTOMER_ID", "GOOGLE_ADS_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET", "GOOGLE_ADS_REFRESH_TOKEN"))


def should_pause(cost_usd, cap_usd, daily_usd, today, end_date):
    """Pause once the next day's worst-case spend could cross the cap, or the test is over.

    Checked once a day, so the cap must hold against a full day of 2x overdelivery.
    """
    return today >= end_date or cost_usd + OVERDELIVERY * daily_usd > cap_usd


def _customer():
    return os.environ["GOOGLE_ADS_CUSTOMER_ID"].replace("-", "")


def _access_token():
    body = urllib.parse.urlencode({
        "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())["access_token"]


def _call(path, payload, token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    login = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
    if login:
        headers["login-customer-id"] = login.replace("-", "")
    req = urllib.request.Request(
        f"https://googleads.googleapis.com/{API_VERSION}/customers/{_customer()}/{path}",
        data=json.dumps(payload).encode(), headers=headers, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Google Ads {path}: {e.code} {e.read().decode()[:800]}") from None


def _mutate(resource, operations, token):
    out = _call(f"{resource}:mutate", {"operations": operations}, token)
    return [r["resourceName"] for r in out.get("results", [])]


def _keyword_ops(ad_group, keywords):
    ops = []
    for match, strip in (("BROAD", ""), ("PHRASE", '"'), ("EXACT", "[]")):
        for kw in keywords.get(match.lower(), []):
            ops.append({"create": {"adGroup": ad_group, "status": "ENABLED",
                                   "keyword": {"text": kw.strip(strip), "matchType": match}}})
    return ops


def launch_campaign(config, total_budget_usd, days):
    """Create budget, campaign, targeting, ad group, keywords and RSA; then enable."""
    token = _access_token()
    customer = f"customers/{_customer()}"
    daily_usd = round(total_budget_usd / days, 2)
    name = config["campaign"]["name"]

    budget = _mutate("campaignBudgets", [{"create": {
        "name": f"{name} budget {date.today().isoformat()}",
        "amountMicros": str(int(daily_usd * 1_000_000)),
        "deliveryMethod": "STANDARD",
        "explicitlyShared": False,
    }}], token)[0]

    campaign = _mutate("campaigns", [{"create": {
        "name": name,
        "status": "PAUSED",
        "advertisingChannelType": "SEARCH",
        "campaignBudget": budget,
        "targetSpend": {},  # Maximize clicks
        "networkSettings": {"targetGoogleSearch": True, "targetSearchNetwork": False,
                            "targetContentNetwork": False, "targetPartnerSearchNetwork": False},
        "containsEuPoliticalAdvertising": "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING",
    }}], token)[0]

    criteria = [{"create": {"campaign": campaign,
                            "location": {"geoTargetConstant": f"geoTargetConstants/{g}"}}}
                for g in GEO_TARGETS]
    criteria.append({"create": {"campaign": campaign,
                                "language": {"languageConstant": f"languageConstants/{LANGUAGE_ENGLISH}"}}})
    _mutate("campaignCriteria", criteria, token)

    ad_group = _mutate("adGroups", [{"create": {
        "name": config["ad_group"]["name"], "campaign": campaign, "status": "ENABLED",
        "type": "SEARCH_STANDARD", "cpcBidMicros": "1000000",
    }}], token)[0]
    _mutate("adGroupCriteria", _keyword_ops(ad_group, config["ad_group"]["keywords"]), token)

    rsa = config["rsa"]
    _mutate("adGroupAds", [{"create": {"adGroup": ad_group, "status": "ENABLED", "ad": {
        "finalUrls": [rsa["final_url"]],
        "responsiveSearchAd": {
            "headlines": [{"text": h} for h in rsa["headlines"][:15]],
            "descriptions": [{"text": d} for d in rsa["descriptions"][:4]],
        }}}}], token)

    _mutate("campaigns", [{"update": {"resourceName": campaign, "status": "ENABLED"},
                           "updateMask": "status"}], token)

    end = date.fromordinal(date.today().toordinal() + days).isoformat()
    record = {"project": config["project"], "customer": customer, "campaign": campaign,
              "cap_usd": total_budget_usd, "daily_usd": daily_usd, "end_date": end,
              "status": "active"}
    state = _load_state()
    state.append(record)
    _save_state(state)
    return record


def enforce_caps(today=None):
    """Pause active campaigns that reached their cap or end date. Returns status lines."""
    state = _load_state()
    active = [c for c in state if c["status"] == "active"]
    if not active:
        return []
    token = _access_token()
    today = today or date.today().isoformat()
    lines = []
    for c in active:
        rows = _call("googleAds:search", {"query": (
            "SELECT metrics.cost_micros, metrics.clicks, metrics.impressions FROM campaign "
            f"WHERE campaign.resource_name = '{c['campaign']}'")}, token).get("results", [])
        m = rows[0].get("metrics", {}) if rows else {}
        cost = int(m.get("costMicros", 0)) / 1_000_000
        clicks = int(m.get("clicks", 0))
        if should_pause(cost, c["cap_usd"], c["daily_usd"], today, c["end_date"]):
            _mutate("campaigns", [{"update": {"resourceName": c["campaign"], "status": "PAUSED"},
                                   "updateMask": "status"}], token)
            c["status"] = "paused"
        c["spent_usd"] = cost
        lines.append(f"{c['project']}: ${cost:.2f} of ${c['cap_usd']:.0f}, {clicks} clicks — {c['status']}")
    _save_state(state)
    return lines


def _load_state():
    if not os.path.exists(STATE_FILE):
        return []
    with open(STATE_FILE) as f:
        return json.load(f)


def _save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)


if __name__ == "__main__":
    # $100 over 7 days = $14.29/day: paused once spend passes 100 - 2 * 14.29.
    assert not should_pause(0, 100, 14.29, "2026-09-27", "2026-10-04")
    assert not should_pause(71, 100, 14.29, "2026-09-30", "2026-10-04")
    assert should_pause(72, 100, 14.29, "2026-09-30", "2026-10-04")
    assert should_pause(10, 100, 14.29, "2026-10-04", "2026-10-04")
    ops = _keyword_ops("ag", {"broad": ["a b"], "phrase": ['"c d"'], "exact": ["[e f]"]})
    assert [o["create"]["keyword"] for o in ops] == [
        {"text": "a b", "matchType": "BROAD"}, {"text": "c d", "matchType": "PHRASE"},
        {"text": "e f", "matchType": "EXACT"}], ops
    print("ok")
