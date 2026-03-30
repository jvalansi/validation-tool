"""
Create and read Tally.so forms for validation campaign signups.
"""

import json
import os
import uuid
import urllib.request
import urllib.error

TALLY_API_KEY = os.environ.get("TALLY_API_KEY")
TALLY_BASE = "https://api.tally.so"


def _tally(method, path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        f"{TALLY_BASE}{path}",
        data=body,
        headers={
            "Authorization": f"Bearer {TALLY_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "validation-tool/1.0",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read()), resp.status
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            return json.loads(body), e.code
        except Exception:
            return {"raw": body.decode(errors="replace")}, e.code


def _uid():
    return str(uuid.uuid4())


def create_signup_form(project_name, description, price_per_year=None):
    """
    Create a Tally form for waitlist signups.

    Returns:
        dict with keys: form_id, form_url, embed_url
    """
    def _saas_price(annual):
        raw = annual / 12
        anchors = [9, 19, 29, 49, 79, 99, 149, 199, 299, 499, 799, 999]
        return min(anchors, key=lambda x: abs(x - raw))

    price_per_mo = _saas_price(price_per_year) if price_per_year else None
    price_str = f"${price_per_mo}/mo" if price_per_mo else "this"

    def label_block(text):
        uid = _uid()
        return {"type": "LABEL", "uuid": uid, "groupUuid": uid, "groupType": "LABEL",
                "payload": {"html": text}}

    title_uid = _uid()
    email_uid = _uid()
    spend_uid = _uid()
    role_uid  = _uid()
    opt_uids  = [_uid() for _ in range(4)]

    spend_options = [
        f"Less than {price_str}",
        f"Around {price_str}",
        f"More than {price_str}",
        "Need to see it first",
    ]

    blocks = [
        {
            "type": "FORM_TITLE",
            "uuid": title_uid,
            "groupUuid": title_uid,
            "groupType": "FORM_TITLE",
            "payload": {"html": f"<b>{project_name} — Early Access Waitlist</b>"},
        },
        label_block("Your work email *"),
        {
            "type": "INPUT_EMAIL",
            "uuid": email_uid,
            "groupUuid": email_uid,
            "groupType": "INPUT_EMAIL",
            "payload": {"isRequired": True},
        },
        {
            "type": "MULTIPLE_CHOICE",
            "uuid": spend_uid,
            "groupUuid": spend_uid,
            "groupType": "MULTIPLE_CHOICE",
            "payload": {
                "question": f"How much would you pay for {project_name}?",
                "isRequired": False,
            },
        },
        *[
            {
                "type": "MULTIPLE_CHOICE_OPTION",
                "uuid": opt_uids[i],
                "groupUuid": spend_uid,
                "groupType": "MULTIPLE_CHOICE",
                "payload": {
                    "text": text,
                    "index": i,
                    "isFirst": i == 0,
                    "isLast": i == len(spend_options) - 1,
                },
            }
            for i, text in enumerate(spend_options)
        ],
        label_block("Your role (optional)"),
        {
            "type": "INPUT_TEXT",
            "uuid": role_uid,
            "groupUuid": role_uid,
            "groupType": "INPUT_TEXT",
            "payload": {"isRequired": False},
        },
    ]

    payload = {
        "name": f"{project_name} Waitlist",
        "status": "PUBLISHED",
        "blocks": blocks,
    }

    result, status = _tally("POST", "/forms", payload)
    if status not in (200, 201):
        raise RuntimeError(f"Tally form creation failed ({status}): {result}")

    form_id = result["id"]
    form_url = f"https://tally.so/r/{form_id}"
    embed_url = f"https://tally.so/embed/{form_id}?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1"

    print(f"Created Tally form: {form_url}")
    return {
        "form_id": form_id,
        "form_url": form_url,
        "embed_url": embed_url,
    }


def get_responses(form_id):
    """
    Fetch all responses from a Tally form.

    Returns list of dicts: {email, spend, role, submitted_at}
    """
    result, status = _tally("GET", f"/forms/{form_id}/responses?limit=100")
    if status != 200:
        raise RuntimeError(f"Failed to fetch responses ({status}): {result}")

    responses = []
    for r in result.get("items", []):
        row = {"submitted_at": r.get("createdAt", "")}
        for field in r.get("fields", []):
            label = field.get("label", "")
            value = field.get("value", "")
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            row[label] = value
        responses.append(row)

    return responses
