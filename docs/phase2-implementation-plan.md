# Phase 2 Implementation Plan

Automate the landing page + signup + monitoring validation pipeline as a standalone `phase2.py`, driven by data already in the Notion Projects table.

## Command Reference

```bash
# One-time machine setup
bash setup_phase2.sh

# Launch a new campaign (deploys landing page, registers campaign)
python phase2.py <notion-page-id> [--days 7] [--dry-run]

# Run daily monitor manually (also runs automatically via cron at 7 AM)
python phase2.py monitor [--dry-run]

# Generate outreach drafts for existing signups (auto-runs on day 5)
python phase2.py <notion-page-id> --outreach [--dry-run]

# Run day-7 kill/build decision (auto-runs on day 7)
python phase2.py <notion-page-id> --decide [--dry-run]
```

---

## Step-by-Step Implementation

### Step 1 — Landing Page Generator ✅

**Input:** Notion page fields (`Project`, `Description`, `Pain/Desire`, `Price/Customer/yr`)
**Output:** Deployed GitHub Pages site at `jvalansi.github.io/validate-<project-slug>`

- Parameterized HTML template (single file, no framework) with hero, feature cards, and multi-step signup form
- Claude generates headline (6–10 words from Pain/Desire), subtitle (≤15 words), and 3 feature cards
- GitHub API creates `validate-<slug>` repo, pushes `index.html`, enables GitHub Pages
- Price anchor rounded to nearest SaaS tier ($9, $19, $29, $49, $79, $99...)
- Inline SVG icons (no emoji — cross-platform safe)

**Key file:** `phase2/landing.py`

---

### Step 2 — Signup Form ✅

**Input:** Project name, price
**Output:** Inline multi-step form on the landing page (email → spend options → role)

- Custom HTML/CSS/JS form embedded directly in the landing page (same dark theme, no iframe)
- Step 1: email input → Step 2: 4 spend option cards + role text field
- Submits via `fetch()` with `mode: no-cors` to a single shared Google Form
- Google Form: `https://forms.gle/1L82UYjVALwZcQ6Y6` (fields: email, spend, role, project)
- Responses stored in Google Sheet: `1UO2fp_kUUj2Go8VZ6nJtdoYhzJDAvrUIVM0Wvp5fg_Y`
- Form entry IDs: email=`49684355`, spend=`441218212`, role=`629651604`, project=`202204044`
- "How much would you pay?" field is **Short answer** (not multiple choice) — accepts any value

**Key file:** `phase2/landing.py` (`GFORM_ACTION`, `GFORM_*` constants)

---

### Step 3 — Google Ads Campaign ⏳ (stub)

**Input:** `Validation Query`, `Pain/Desire`, landing page URL, daily budget
**Output:** Campaign ID, ad group ID

- Create Search campaign via Google Ads API
- Generate keyword list from `Validation Query` + `Pain/Desire` using Claude
- Generate 3 ad variants using Claude (headline from pain, solution, CTA)
- Set daily budget, geo targeting, device targeting

**APIs needed:** Google Ads API (requires developer token + OAuth) — not yet implemented

---

### Step 4 — Daily Monitor ✅

**Input:** Active campaigns from `data/campaigns.json`
**Output:** Slack message to `#proj-project-validation`

Runs daily at 7 AM via cron. For each active campaign:
- Reads signups from Google Sheets (filtered by project name)
- Computes: total signups, pace/day, projected 7-day total
- Posts summary + kill/continue recommendation to Slack
- **Day 5:** auto-triggers outreach drafts
- **Day 7:** auto-triggers kill/build decision, marks campaign as ended

**Key file:** `phase2/monitor.py`

---

### Step 5 — Outreach Drafts ✅

**Input:** Signup responses (email, spend, role) from Google Sheets
**Output:** Personalised outreach email draft per signup, posted as Slack thread

- Claude generates a 4–6 sentence cold email per signup
- Uses spend intent and role for personalisation
- Includes soft pre-order ask at the monthly founder price
- Posted to `#proj-project-validation` as a thread for manual review + sending
- Auto-triggered on day 5 by the monitor cron

**Key file:** `phase2/outreach.py`

---

### Step 6 — Day 7 Decision ✅

**Input:** Total signups + spend intent breakdown
**Output:** Kill/build verdict posted to Slack + Notion `סטטוס` updated

- **≥3 strong signals** (Around/More than price): verdict = `build` → Notion status → `building`
- **≥5 signups, <3 strong**: verdict = `validate_more` → Notion status → `validating`
- **<5 signups**: verdict = `kill` → Notion status → `killed`
- Auto-triggered on day 7 by the monitor cron

**Key file:** `phase2/decision.py`

---

## Credentials & Setup

| Service | Credential | Status |
|---|---|---|
| GitHub | `GH_TOKEN` | ✅ in `.env` |
| Notion | `NOTION_TOKEN` | ✅ in `.env` |
| Slack | `SLACK_BOT_TOKEN` | ✅ in `.env` |
| Google Sheets (read) | Service account key | ✅ `/home/ubuntu/google-service-account.json` |
| Google Forms (update) | Same service account | ✅ form shared with `gclaude@optimum-lodge-278819.iam.gserviceaccount.com` |
| Google Ads | Developer token + OAuth | ❌ not yet implemented |

---

## File Structure

```
validation-tool/
  phase2.py              # main entry point + CLI
  setup_phase2.sh        # one-time setup: checks env, installs deps, sets up cron
  data/
    campaigns.json       # active/ended campaign state (auto-managed)
  phase2/
    landing.py           # HTML generator + GitHub Pages deployment
    monitor.py           # daily metrics, Sheets reader, auto-triggers
    outreach.py          # Claude-generated outreach drafts → Slack
    decision.py          # day-7 kill/build logic → Slack + Notion
    forms.py             # (legacy Tally helpers, no longer used in main flow)
  docs/
    phase2-implementation-plan.md   # this file
```

---

## Automated Campaign Lifecycle

```
Day 0  →  python phase2.py <page-id>   Deploy landing page, register campaign
Day 1–4 →  cron 7 AM                   Daily Slack summary (signups, pace, projection)
Day 5   →  cron 7 AM (auto)            Outreach drafts posted to Slack
Day 6   →  cron 7 AM                   Final day summary
Day 7   →  cron 7 AM (auto)            Kill/build decision → Slack + Notion updated
```

---

## What's Left

- **Google Ads integration** — most complex; can validate manually without it for now
- **Multi-project Notion view** — show all campaigns and their status in one Notion dashboard
