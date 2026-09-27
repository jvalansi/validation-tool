"""
Post validation updates to the #validation-tool Discord channel.

Uses the cc-connect bot token, so no separate bot is needed. Slack is no longer
used. Falls back to stdout when the token can't be read.
"""

import json
import os
import re
import urllib.request

CHANNEL_ID = os.environ.get("VALIDATION_DISCORD_CHANNEL_ID", "1553614469584654336")
CC_CONFIG = os.path.expanduser("~/.cc-connect/config.toml")
LIMIT = 2000  # Discord message length cap


def _token():
    try:
        s = open(CC_CONFIG).read()
        m = re.search(r"\[projects\.platforms\.options\](.*?)(\n\[|\Z)", s, re.S)
        return re.search(r'token\s*=\s*"([^"]+)"', m.group(1)).group(1)
    except Exception:
        return None


def post(text, thread_ts=None):
    """Send text (split to Discord's 2000-char limit). thread_ts is accepted for old Slack callers and ignored."""
    token = _token()
    if not token:
        print(f"[notify] {text}")
        return None
    last = None
    for i in range(0, len(text), LIMIT):
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages",
            data=json.dumps({"content": text[i:i + LIMIT]}).encode(),
            headers={"Authorization": f"Bot {token}", "Content-Type": "application/json",
                     "User-Agent": "validation-tool"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                last = json.loads(r.read()).get("id")
        except Exception as e:
            print(f"[notify] Discord post failed: {e}\n{text}")
    return last
