#!/usr/bin/env python3
"""Runnable check for the incumbent-detection logic. No network required.

    python phase1/test_validation_tool.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validation_tool import (
    _parse_funding, _assess_competition, _host, _classify_hosts,
    _unit_economics, MIN_EV_PER_CUSTOMER_USD, _query_tokens, _restriction_match,
    _extract_prices, _is_non_vendor, _apply_claude_competition, _apply_tam_source, _apply_price_source, _annualize_one_time,
)

# --- _parse_funding: funding language required -------------------------------
assert _parse_funding("Ownwell Raises $50 Million To Grow Its Property Tax Fintech") == 50_000_000
assert _parse_funding("raised a $1.5 billion Series D") == 1_500_000_000
# "$400 million saved for customers" is a result, not a raise
assert _parse_funding("Ownwell has saved customers more than $400 million") is None
assert _parse_funding("") is None

# --- _host -------------------------------------------------------------------
assert _host("https://www.ownwell.com/pricing") == "ownwell.com"
assert _host("not a url") == ""

# --- papers, code hosts and universities are not vendors ----------------------
for h in ("frontiersin.org", "pmc.ncbi.nlm.nih.gov", "elifesciences.org", "github.com",
          "spikeinterface.github.io", "sccn.ucsd.edu", "ucl.ac.uk", "unimelb.edu.au", "en.wikipedia.org"):
    assert _is_non_vendor(h), h
for h in ("encevis.com", "cleaneeg.com", "catalystneuro.com", "ownwell.com", "emotiv.com"):
    assert not _is_non_vendor(h), h

# --- the regression this was built for ---------------------------------------
# Property tax appeals: absent from Product Hunt, but a $50M-funded incumbent
# and several flat-fee vendors are actively selling. Must NOT read as a gap.
proptax = _assess_competition(
    {"operators_found": 3, "max_funding_usd": 50_000_000},
    {"existing_products": 0},
)
assert proptax["level"] == "funded", proptax
assert "50M" in proptax["negative"][0], proptax
# A funded competitor is evidence the market is real — it caps upside, not to zero.
assert proptax["positive"], proptax

# Only a category owner floors the signal.
owner = _assess_competition({"operators_found": 4, "max_funding_usd": 434_000_000}, {"existing_products": 0})
assert owner["level"] == "dominant", owner
assert owner["positive"] == [], owner

# Funding plus a full field is crowded, not merely "funded" — money is not the only barrier.
both = _assess_competition({"operators_found": 15, "max_funding_usd": 50_000_000}, {"existing_products": 0})
assert both["level"] == "crowded", both
assert both["positive"] == [], both

# One vendor is "open", not "contested" — barely served, still proven.
lone = _assess_competition({"operators_found": 1, "max_funding_usd": None}, {"existing_products": 0})
assert lone["level"] == "open", lone
assert lone["negative"] == [], lone

# Absence of vendors is a negative (unproven), never a positive.
empty = _assess_competition({"operators_found": 0, "max_funding_usd": None}, {"existing_products": 0})
assert empty["level"] == "none_found", empty
assert empty["positive"] == [], empty

# A few small vendors and no big raise is the genuinely promising shape.
wedge = _assess_competition({"operators_found": 3, "max_funding_usd": None}, {"existing_products": 1})
assert wedge["level"] == "contested", wedge
assert len(wedge["positive"]) == 1 and wedge["negative"] == [], wedge

# Many vendors, none funded, still reads as crowded.
crowded = _assess_competition({"operators_found": 9, "max_funding_usd": None}, {"existing_products": 6})
assert crowded["level"] == "crowded", crowded
assert len(crowded["negative"]) == 2, crowded

# --- _unit_economics: price is observed, customer counts are assumed ----------
none = _unit_economics([], "mass")
assert none["price_anchor_usd"] is None, none
assert none["ev_per_customer_annual_usd"] is None, none
assert none["conservative_mrr"] == "", none  # no price -> no invented range

cheap = _unit_economics([{"monthly_equiv": 4.0, "period": "monthly"}], "niche")
assert cheap["ev_per_customer_annual_usd"] == round(4.0 * 12 * 0.8), cheap
assert cheap["below_acquisition_floor"] is True, cheap

rich = _unit_economics([{"monthly_equiv": 50.0, "period": "monthly"}], "mid")
assert rich["ev_per_customer_annual_usd"] == 480, rich
assert rich["below_acquisition_floor"] is False, rich
assert rich["conservative_mrr"] == "$1000", rich  # $50/mo x 20 customers

# Search volume must not move revenue: same price, different TAM tier, same EV.
assert (_unit_economics([{"monthly_equiv": 50.0, "period": "monthly"}], "mass")["ev_per_customer_annual_usd"]
        == rich["ev_per_customer_annual_usd"])
assert MIN_EV_PER_CUSTOMER_USD == 200

# --- _classify_hosts: who owns the results page ------------------------------
owned = _classify_hosts(
    ["ownwell.com", "appealdesk.com", "cutmytaxes.com", "nytimes.com"],
    incumbent_hosts={"ownwell.com", "appealdesk.com", "cutmytaxes.com"},
)
assert owned["vendor_share"] == 0.75, owned
assert "paid acquisition" in owned["read"], owned

open_serp = _classify_hosts(["cookcountyassessor.gov", "reddit.com", "someblog.com"], incumbent_hosts=set())
assert open_serp["breakdown"] == {"vendor": 0, "government": 1, "forum": 1, "content": 1}, open_serp
assert "organic entry plausible" in open_serp["read"], open_serp

# --- regulatory matching: needs a restriction term AND query overlap ---------
tokens = _query_tokens("property tax appeal service")
assert tokens == ["property", "appeal"], tokens  # "tax" too short, "service" a stopword

ptab = ("Frequently Asked Questions - Property Tax Appeal Board. PTAB rules prohibit accountants, "
        "tax representatives and others not qualified to practice law from appearing")
assert _restriction_match(ptab, tokens)[0] == ["not qualified to practice"], _restriction_match(ptab, tokens)

# Generic state-bar boilerplate must not flag: restriction term, no query overlap.
boilerplate = "An Unauthorized Practice of Law Complaint can be submitted to the Virginia State Bar"
assert _restriction_match(boilerplate, tokens) == ([], []), _restriction_match(boilerplate, tokens)

# Query words with no restriction language must not flag either.
assert _restriction_match("file a property tax appeal with the county board", tokens) == ([], [])

# --- price periods: a bare "$49" is one-time, not $49/mo ---------------------
periods = {p["raw"]: p["period"] for p in _extract_prices(["Flat $49, every time", "$936 per year", "$20/month"])}
assert periods["$49"] == "unknown", periods
assert periods["$936 per year"] == "annual", periods
assert periods["$20/month"] == "monthly", periods

# AppealDesk's $49 flat fee must not be annualized into $470/yr of revenue.
one_time = _unit_economics([{"monthly_equiv": 49.0, "period": "unknown"}], "mid")
assert one_time["price_is_recurring"] is False, one_time
assert one_time["ev_per_customer_annual_usd"] == round(49 * 0.8), one_time
assert one_time["below_acquisition_floor"] is True, one_time

# An explicit period wins over undated noise scraped from the same page.
mixed = _unit_economics(
    [{"monthly_equiv": 49.0, "period": "unknown"}, {"monthly_equiv": 30.0, "period": "monthly"}], "mid")
assert mixed["price_is_recurring"] is True and mixed["price_anchor_usd"] == 30.0, mixed

# --- a failed search is "unknown", never "no competitors" --------------------
blind = _assess_competition({"search_failed": True, "operators_found": 0}, {"existing_products": 0})
assert blind["level"] == "unknown", blind
assert "not absent" in blind["negative"][0], blind

# --- a single observed price is too thin to kill an idea --------------------
thin = _unit_economics([{"monthly_equiv": 49.0, "period": "unknown"}], "mid")
assert thin["price_observations"] == 1, thin
solid = _unit_economics(
    [{"monthly_equiv": 5.0, "period": "monthly"}, {"monthly_equiv": 7.0, "period": "monthly"}], "mid")
assert solid["price_observations"] == 2 and solid["below_acquisition_floor"] is True, solid

# --- one failed probe makes competition unknown, not absent -------------------
assert _assess_competition({"operators_found": 7, "probes_failed": 1}, {})["level"] == "unknown"

# --- Claude's competition grade replaces the heuristic only when the data backs it --
def _report():
    return {"sources": {"incumbents": {"operators": [{"host": "daily.dev", "url": "https://daily.dev/x",
                                                     "snippet": "Cursor vs Copilot vs Claude Code pricing"}]}},
            "summary": {"competition": "contested", "verdict": "validate further", "signal_count": 3}}
r = _report()
_apply_claude_competition(r, {"competition_level": "dominant",
                              "competitors": [{"name": "Cursor", "evidence_url": "https://daily.dev/x"}]})
assert r["summary"]["competition"] == "dominant" and r["summary"]["verdict"].startswith("crowded"), r
r = _report()  # cited snippet doesn't name the competitor → ignored
_apply_claude_competition(r, {"competition_level": "dominant",
                              "competitors": [{"name": "Tabnine", "evidence_url": "https://daily.dev/x"}]})
assert r["summary"]["competition"] == "contested", r
r = _report()
r["summary"]["verdict"] = "unviable — value per customer below the acquisition floor"
_apply_claude_competition(r, {"competition_level": "open", "competitors": [
    {"name": "Copilot", "evidence_url": "https://daily.dev/x"}]})
assert r["summary"]["competition"] == "open" and r["summary"]["verdict"].startswith("unviable"), r

# --- _apply_tam_source: a TAM counts as sourced only if its snippet has the quoted count ---
src = {"sources": {"market_size": {"results": [{"title": "Forex stats", "url": "https://x.com/fx",
                                                "snippet": "There are about 13.9 million retail forex traders worldwide"}]}}}
a = {"tam_source": "https://x.com/fx", "tam_source_quote": "13.9 million"}
_apply_tam_source(src, a)
assert a["tam_sourced"] and a["tam_source"] == "https://x.com/fx", a
for bad in ({"tam_source": "https://x.com/fx", "tam_source_quote": "50 million"},   # not in the snippet
            {"tam_source": "https://other.com", "tam_source_quote": "13.9 million"},  # not in the research data
            {"tam_source": "https://x.com/fx", "tam_source_quote": "million"},       # no number
            {"tam_source": None, "tam_source_quote": None}):
    _apply_tam_source(src, bad)
    assert not bad["tam_sourced"] and bad["tam_source"] is None, bad

# --- _apply_price_source: quote must be on the cited page and within 10x of the annual price ---
rep = {"sources": {}, "revenue_estimate": {"competitor_prices_found": [
    {"raw": "$20/mo", "url": "https://v.com/pricing", "snippet": "Pro plan $20/month per seat"}]}}
a = {"price_source": "https://v.com/pricing", "price_source_quote": "$20/month", "price_per_customer_annual": 1000}
_apply_price_source(rep, a)
assert a["price_sourced"], a  # $240/yr vs $1000: per-seat, within 10x
rep["revenue_estimate"]["competitor_prices_found"][0]["snippet"] = "Meter costs $25 per screen per month"
a = {"price_source": "https://v.com/pricing", "price_source_quote": "$25 per screen per month", "price_per_customer_annual": 1000}
_apply_price_source(rep, a)
assert a["price_sourced"], a  # the period comes after the unit
for bad in ({"price_source": "https://v.com/pricing", "price_source_quote": "$20/month", "price_per_customer_annual": 10000},
            {"price_source": "https://v.com/pricing", "price_source_quote": "$99/month", "price_per_customer_annual": 1000},
            {"price_source": None, "price_source_quote": None, "price_per_customer_annual": 1000}):
    _apply_price_source(rep, bad)
    assert not bad["price_sourced"] and bad["price_source"] is None, bad

# --- _source_tam: TAM = cited population x share tier, at 2 significant figures ---
import validation_tool as vt
_calls = iter([{"tam_source": "https://s.com/n", "tam_source_quote": "4.3 million", "count": 4_300_000},
               {"share": "10%", "reason": "shops that take orders"}])
vt._market_size_search = lambda g: {"results": [{"title": "SMB stats", "url": "https://s.com/n",
                                                  "snippet": "There are 4.3 million small businesses"}]}
vt._claude_json = lambda prompt: next(_calls)
a = {"customer_group": "small businesses", "price_per_customer_annual": 1000}
vt._source_tam({"sources": {}, "query": "Qordr"}, a)
assert a["tam_sourced"] and a["tam_customers"] == 1_000_000 and a["value"] == 1_000_000_000, a
_calls = iter([{"tam_source": "https://s.com/n", "tam_source_quote": "4.3 million", "count": 4_300_000}, {"share": "half"}])
a = {"customer_group": "small businesses", "tam_customers": 10**6}
vt._source_tam({"sources": {}, "query": "Qordr"}, a)
assert not a["tam_sourced"] and a["tam_customers"] == 10**6, a  # no valid share: keep the guess, flagged

# --- _extract_prices: thousands separators ---
ps = _extract_prices(["Swim spas cost $25,000 to $70,000; a tether is $49/month"])
assert [p["monthly_equiv"] for p in ps] == [25000, 70000, 49], ps

# --- _annualize_one_time: a one-time sale counts once in the x10-years Value ---
a = {"price_type": "one_time", "price_per_customer_annual": 10_000}
_annualize_one_time(a)
assert a["price_per_customer_annual"] == 1_000 and a["price_one_time"] == 10_000, a
a = {"price_type": "recurring", "price_per_customer_annual": 1_000}
_annualize_one_time(a)
assert a["price_per_customer_annual"] == 1_000 and "price_one_time" not in a, a

# unsourced TAM is Claude's guess / 10; sourced TAM is left alone
a = {"tam_customers": 10_000_000}
vt._discount_unsourced_tam(a)
assert a["tam_customers"] == 1_000_000 and a["tam_guess"] == 10_000_000, a
a = {"tam_customers": 45_000, "tam_sourced": True}
vt._discount_unsourced_tam(a)
assert a["tam_customers"] == 45_000 and "tam_guess" not in a, a

# a run that finds no count keeps the population x share stored on the page
sys.path.insert(0, os.path.dirname(__file__))
from notion_validate import reuse_prior_tam
props = {"TAM Population": {"number": 450_000}, "TAM Share": {"number": 0.1}, "TAM Source": {"url": "https://x"},
         "TAM Source Quote": {"rich_text": [{"plain_text": "450,000"}]}, "Customer Group": {"rich_text": [{"plain_text": "day traders"}]}}
c = {"tam_customers": 1_000_000}
reuse_prior_tam(c, props)
assert c["tam_customers"] == 100_000 and c["tam_sourced"] and c["tam_share"] == "10%" and c["customer_group"] == "day traders", c
c = {"tam_customers": 8_500, "tam_sourced": True}
reuse_prior_tam(c, props)
assert c["tam_customers"] == 8_500 and "tam_reused" not in c, c

# competitors from the category search and earlier runs raise the grade, never lower it, and leave probability alone
r = {"summary": {"competition": "contested", "verdict": "weak signal — reconsider or reframe"}}
a = {"suggested_probability": 1.0, "competitors": [{"name": "VantagePoint"}, {"name": "Forexsignals"}]}
vt.merge_competitors(r, a, [{"name": n} for n in ("forexsignals", "A", "B", "C")])
assert len(a["competitors"]) == 5 and r["summary"]["competition"] == "crowded" and a["suggested_probability"] == 1.0, (r, a)
r = {"summary": {"competition": "crowded"}}
a = {"competitors": [{"name": "A"}]}
vt.merge_competitors(r, a, [])
assert r["summary"]["competition"] == "crowded", r
assert vt._competitors_level([{"name": "A", "funding_usd": 2e8}]) == "dominant"
assert vt._cited([{"name": "Foo", "evidence_url": "u"}, {"name": "Bar", "evidence_url": "u"}], {"u": "foo signals"}) == [
    {"name": "Foo", "evidence_url": "u", "why": None, "funding_usd": None}]

# agent_review.snap: steps, one-time /10, and sources only when the quote is on the page
from agent_review import snap
v = snap({"population": 4_300_000, "share": 0.1, "population_source_url": "u", "population_quote": "4.3 million", "tam": 5,
          "price": 20_000, "price_type": "one_time", "price_source_url": "u", "price_quote": "$20,000", "competition": "funded",
          "probability": 0.05}, check=lambda url, quote: True)
assert (v["tam"], v["tam_sourced"], v["price"], v["price_one_time"], v["price_sourced"], v["probability"]) == (
    1_000_000, True, 1_000, 10_000, True, 0.03), v
v = snap({"population": 4_300_000, "share": 0.1, "tam": 3_000, "price": 240, "competition": "bogus", "probability": 2},
         check=lambda url, quote: False)
assert (v["tam"], v["tam_sourced"], v["price"], v["competition"], v["probability"]) == (1_000, False, 100, "none_found", 0.3), v

print("all checks passed")

# The Notion ROI formula, as agent_review.roi recomputes it for rescoring
from agent_review import roi as _roi
assert abs(_roi(50_000, 100, "contested", 0.1, 1, 0.75) - 50_000 * 100 * 0.05 * 10 * 0.1 / 4000 * 2 / 1.25) < 1e-9
assert _roi(1000, 10, "open", 0.1, 2, None) == 1000 * 10 * 0.1 * 10 * 0.1 / 8000
print("ok roi")

from agent_review import parse_reply as _parse_reply
assert _parse_reply('Here: {"tam": 5, "c": [{"a": 1}]}\nSources: {x}') == {"tam": 5, "c": [{"a": 1}]}
print("ok parse_reply")
