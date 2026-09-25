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
    _extract_prices, _is_non_vendor,
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

print("all checks passed")
