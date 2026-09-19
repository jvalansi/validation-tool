#!/usr/bin/env python3
"""Runnable check for the incumbent-detection logic. No network required.

    python phase1/test_validation_tool.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validation_tool import _parse_funding, _assess_competition, _host

# --- _parse_funding: funding language required -------------------------------
assert _parse_funding("Ownwell Raises $50 Million To Grow Its Property Tax Fintech") == 50_000_000
assert _parse_funding("raised a $1.5 billion Series D") == 1_500_000_000
# "$400 million saved for customers" is a result, not a raise
assert _parse_funding("Ownwell has saved customers more than $400 million") is None
assert _parse_funding("") is None

# --- _host -------------------------------------------------------------------
assert _host("https://www.ownwell.com/pricing") == "ownwell.com"
assert _host("not a url") == ""

# --- the regression this was built for ---------------------------------------
# Property tax appeals: absent from Product Hunt, but a $50M-funded incumbent
# and several flat-fee vendors are actively selling. Must NOT read as a gap.
proptax = _assess_competition(
    {"operators_found": 3, "max_funding_usd": 50_000_000},
    {"existing_products": 0},
)
assert proptax["level"] == "funded_incumbent", proptax
assert proptax["positive"] == [], proptax
assert "50M" in proptax["negative"][0], proptax

# Absence of vendors is a negative (unproven), never a positive.
empty = _assess_competition({"operators_found": 0, "max_funding_usd": None}, {"existing_products": 0})
assert empty["level"] == "none_found", empty
assert empty["positive"] == [], empty

# A few small vendors and no big raise is the genuinely promising shape.
wedge = _assess_competition({"operators_found": 2, "max_funding_usd": None}, {"existing_products": 1})
assert wedge["level"] == "contested", wedge
assert len(wedge["positive"]) == 1 and wedge["negative"] == [], wedge

# Many vendors, none funded, still reads as crowded.
crowded = _assess_competition({"operators_found": 7, "max_funding_usd": None}, {"existing_products": 6})
assert crowded["level"] == "crowded", crowded
assert len(crowded["negative"]) == 2, crowded

print("all checks passed")
