# Phase 2 Implementation Plan

Automate the Google Ads + Landing Page validation pipeline as a new command in `validation_tool.py` (or a standalone `phase2.py`), driven by data already in the Notion Projects table.

## New Command

```bash
python phase2.py <notion-page-id> [--budget 100] [--days 7] [--dry-run]
```

Reads from Notion, spins up all the pieces, monitors daily, reports to Slack.

---

## Step-by-Step Implementation

### Step 1 — Landing Page Generator

**Input:** Notion page fields (`Project`, `Description`, `Pain/Desire`, `Price/Customer/yr`)
**Output:** A deployed GitHub Pages site at `jvalansi.github.io/validate-<project-slug>`

- Create a parameterized HTML template (single file, no framework) with hero, CTA, and form embed
- Use GitHub API to create a new repo `validate-<project-slug>`, push the rendered HTML as `index.html`, enable GitHub Pages
- Embed a Typeform or Google Form for email + spend collection

**APIs needed:** GitHub API (already authenticated via `GH_TOKEN`)

---

### Step 2 — Signup Form

**Input:** Project name, spend question
**Output:** Form URL to embed in landing page

Two options:
- **Google Forms API** — free, no extra credentials, responses go to Google Sheets
- **Typeform API** — cleaner UX, requires `TYPEFORM_TOKEN`

Recommendation: Google Forms — simpler auth, responses readable via Google Sheets API.

**APIs needed:** Google Forms API + Google Sheets API (OAuth or service account)

---

### Step 3 — Google Ads Campaign

**Input:** `Validation Query`, `Pain/Desire`, landing page URL, daily budget
**Output:** Campaign ID, ad group ID

- Create Search campaign via Google Ads API
- Generate keyword list from `Validation Query` + `Pain/Desire` using Claude (broad + exact match)
- Generate 3 ad variants using Claude (headline from pain, solution, CTA)
- Set daily budget, geo targeting, device targeting

**APIs needed:** Google Ads API (requires Google Ads developer token + OAuth)

---

### Step 4 — Daily Monitor

**Input:** Campaign ID, form ID
**Output:** Slack message to `#proj-<project-slug>`

Runs daily via cron (same pattern as `reddit-tool/monitor.py`):
- Pull Google Ads metrics: impressions, clicks, CTR, CPC, spend
- Pull form responses: new signups, spend answers
- Compute: spend per signup, days remaining, projected total signups
- Post summary to Slack with kill/continue recommendation

**APIs needed:** Google Ads API, Google Sheets API (for form responses)

---

### Step 5 — Outreach Drafts (Day 4–5)

**Input:** Signup responses (name, email, spend)
**Output:** Personalised outreach message per signup, posted to Slack for review

- Claude generates a DM/email draft per signup using their stated spend and the project's `Pain/Desire`
- Posted to Slack as a thread for the user to copy/send manually
- Includes a pre-order ask at `Price/Customer/yr ÷ 12` per month

**APIs needed:** Google Sheets API (to read responses), Claude API

---

### Step 6 — Day 7 Decision

**Input:** Total signups, pre-orders, spend
**Output:** Kill/build recommendation posted to Slack + Notion status updated

- If <5 signups: update Notion `סטטוס` → `killed`, suggest next project by ROI
- If 3+ pre-orders: update `סטטוס` → `building`, post next steps to Slack
- Pause Google Ads campaign

---

## Credentials Needed

| Service | Credential | Status |
|---|---|---|
| GitHub | `GH_TOKEN` | ✅ already in `.env` |
| Notion | `NOTION_TOKEN` | ✅ already in `.env` |
| Slack | `SLACK_BOT_TOKEN` | ✅ already in `.env` |
| Google Ads | Developer token + OAuth | ❌ needs setup |
| Google Forms/Sheets | OAuth or service account | ❌ needs setup |
| Typeform | `TYPEFORM_TOKEN` | ❌ optional alternative to Google Forms |

---

## Build Order

1. **Landing page generator** — highest leverage, no new credentials needed (GitHub API)
2. **Google Forms + Sheets** — free, one-time OAuth setup
3. **Daily monitor** — simple cron once forms are set up
4. **Google Ads** — most complex auth, do last; can run ads manually while pipeline is being built
5. **Outreach drafts** — Claude generation, straightforward once signups are flowing
6. **Day 7 decision** — automatic once monitor is running

---

## File Structure

```
validation-tool/
  phase2.py              # main entry point
  phase2/
    landing.py           # GitHub Pages deployment
    forms.py             # Google Forms creation
    ads.py               # Google Ads campaign management
    monitor.py           # daily metrics + Slack reporting
    outreach.py          # Claude-generated DM drafts
    decision.py          # day 7 kill/build logic
  docs/
    google-ads-validation.md   # process overview
    phase2-implementation-plan.md  # this file
```
