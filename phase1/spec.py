#!/usr/bin/env python3
"""
Product spec per idea: a "Spec" section in the idea's Notion page, written by a Claude Code agent that searches as
it goes. It pins down the product - who it's for, the input it takes, the output it gives, the states a visitor can
be in, what's in and out of scope - so phase 1 scores that product and build_mvp builds the same one. Sections follow
GitHub Spec Kit's spec template (scenarios, scope, success criteria, at most 3 [NEEDS CLARIFICATION]) plus explicit
input/output. Price isn't in it: phase 1 prices the spec.

The Notion section is the source of truth: edit it to change the product. Re-running (--rewrite) starts from the
current section, keeps every decision in it and only fills gaps, so answered questions stick.

Usage: python spec.py <page-id> [--rewrite] [--dry-run]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "phase0"))
from notion_validate import get_page_blocks, notion_get, notion_patch, notion_delete  # noqa: E402
from analyze import PROFILE  # noqa: E402

HEADING = "Spec"
SECTIONS = ("Problem", "Customer", "Input", "Output", "States", "Scenarios", "Scope", "Success metric",
            "Open questions")

PROMPT = """Write the product spec for this idea from the validation-tool ideas DB. It decides what gets scored (market size,
price, competition) and what an agent builds next as a paid web app, so it must say exactly what the product is.
Search the web as you go (who has this problem, how they solve it today, what existing products take as input and
give as output) and decide; don't ask me anything except through Open questions.

The idea (Notion row):
- Name: {name}
- Description: {description}
- Pain/desire: {pain}
- Customer group: {customers}
- Competitors: {competitors}
- Reviewer's note: {review}
{current}
Builder: {profile}

Decide the market by where the most paying customers are that this product can serve, not by the language of the
idea's name (that only says where the idea came from). Price is set later from this spec: leave it out.

Reply with ONLY these Markdown sections, each a "### " heading, short and concrete:
### Problem
Who hurts, what the pain is, and how they deal with it today (with a source link).
### Customer
The segment, the market (countries) and the language(s) the product works in.
### Input
Exactly what the user gives (a link, an address, a question, a file, form fields), and one real example.
### Output
Exactly what they get back, and what it would look like for the example.
### States
The states a visitor can be in that change what they see or can do (e.g. first visit, free uses left, out of free
uses, subscribed), one bullet each.
### Scenarios
3-5 numbered "Given <state>, When <input>, Then <output>" lines, most important first; the first alone is a usable MVP.
### Scope
- In: what the MVP does
- Out: what it deliberately doesn't do (other markets, inputs, features)
- Cut: what goes first if the build runs long
### Success metric
What phase 2 (paid search clicks sent to the app) should count to call it working, e.g. free uses and paid
checkouts per click.
### Open questions
At most 3 bullets, only where the answer changes the product (market, input, output):
"[NEEDS CLARIFICATION: <question>] Default: <what the build does if nobody answers>". "None" if there are none."""


def text(prop):
    return "".join(t["plain_text"] for t in prop.get(prop.get("type"), []) or []) if prop else ""


def block_text(b):
    return "".join(x.get("plain_text", "") for x in b.get(b["type"], {}).get("rich_text", []))


def spec_blocks(page_id):
    """The blocks of the page's Spec section (heading included), [] if it has none."""
    out, inside = [], False
    for b in get_page_blocks(page_id):
        if b["type"] == "heading_2":
            inside = block_text(b).strip() == HEADING
        if inside:
            out.append(b)
    return out


def read_spec(page_id):
    """The Spec section as Markdown (without its heading), "" if there is none."""
    prefix = {"heading_3": "### ", "bulleted_list_item": "- ", "numbered_list_item": "1. ", "to_do": "- "}

    def lines(blocks, depth=0):
        for b in blocks:
            yield "  " * depth + prefix.get(b["type"], "") + block_text(b)
            if b.get("has_children"):
                yield from lines(get_page_blocks(b["id"]), depth + 1)
    return "\n".join(lines(spec_blocks(page_id)[1:])).strip()


def rich(line):
    """**bold** and [text](url) -> Notion rich text."""
    parts = []
    for m in re.finditer(r"\*\*(.+?)\*\*|\[([^\]]+)\]\((https?://[^)\s]+)\)|([^*\[]+|[*\[])", line):
        bold, label, url, plain = m.groups()
        if bold:
            parts.append({"text": {"content": bold}, "annotations": {"bold": True}})
        elif label:
            parts.append({"text": {"content": label, "link": {"url": url}}})
        else:
            parts.append({"text": {"content": plain}})
    return [p for p in parts if p["text"]["content"]][:100]


def to_blocks(md):
    """The agent's Markdown -> Notion blocks (### headings, bullets, numbered lines, paragraphs); indented list items
    become children of the item above them."""
    blocks, stack = [], []  # stack: (indent, block) of the open list items
    for line in md.splitlines():
        s = line.strip()
        if not s:
            continue
        indent = len(line) - len(line.lstrip())
        if s.startswith("#"):
            kind, s = "heading_3", s.lstrip("#").strip()
        elif re.match(r"[-*] ", s):
            kind, s = "bulleted_list_item", s[2:]
        elif re.match(r"\d+[.)] ", s):
            kind, s = "numbered_list_item", s.split(" ", 1)[1]
        else:
            kind = "paragraph"
        block = {"type": kind, kind: {"rich_text": rich(s[:2000])}}
        while stack and (stack[-1][0] >= indent or kind == "heading_3"):
            stack.pop()
        if stack and kind != "heading_3":
            stack[-1][1][stack[-1][1]["type"]].setdefault("children", []).append(block)
        else:
            blocks.append(block)
        if kind.endswith("list_item"):
            stack.append((indent, block))
    return blocks


def check(md):
    """Every section present, in order; raises otherwise so a malformed spec never replaces a good one."""
    found = [h.strip() for h in re.findall(r"^###\s+(.+)$", md, re.M)]
    missing = [s for s in SECTIONS if s not in found]
    if missing:
        raise ValueError(f"spec is missing sections: {', '.join(missing)}")
    return md[md.find("###"):].strip()


def ask(prompt, timeout=1800):
    claude = shutil.which("claude") or "/home/ubuntu/.local/bin/claude"
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}  # the CLI runs on the subscription
    out = subprocess.run([claude, "-p", prompt, "--output-format", "json", "--model", "claude-opus-5-5",
                          "--allowedTools", "WebSearch,WebFetch"],
                         capture_output=True, text=True, timeout=timeout, env=env, cwd="/tmp")
    return json.loads(out.stdout).get("result", "")


def prompt_for(page, current=""):
    p = page["properties"]
    try:
        competitors = ", ".join(f"{c['name']} ({c.get('why', '')})" for c in json.loads(text(p.get("Competitors")) or "[]"))
    except ValueError:
        competitors = ""
    cur = ("\nThe current spec, which the owner may have edited: keep every decision and answer in it, fill gaps, "
           "fix only what's wrong, and drop questions it already answers:\n" + current + "\n") if current else ""
    return PROMPT.format(name=text(p["Project"]), description=text(p.get("Description")) or "-",
                         pain=text(p.get("Pain/Desire")) or "-", customers=text(p.get("Customer Group")) or "-",
                         competitors=competitors or "none recorded", review=text(p.get("Review Note")) or "-",
                         current=cur, profile=PROFILE)


def write_spec(page_id, md):
    """Replaces the page's Spec section (appended at the end if it has none)."""
    for b in spec_blocks(page_id):
        notion_delete(f"blocks/{b['id']}")
    blocks = [{"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": HEADING}}]}}] + to_blocks(md)
    for i in range(0, len(blocks), 100):
        notion_patch(f"blocks/{page_id}/children", {"children": blocks[i:i + 100]})


def spec(page_id, rewrite=False, dry_run=False):
    """Writes the page's spec (or rewrites it from the current one); returns the Markdown."""
    current = read_spec(page_id)
    if current and not rewrite:
        return current
    md = check(ask(prompt_for(notion_get(f"pages/{page_id}"), current)))
    if not dry_run:
        write_spec(page_id, md)
    return md


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page_id")
    ap.add_argument("--rewrite", action="store_true", help="rewrite an existing spec, keeping its decisions")
    ap.add_argument("--dry-run", action="store_true", help="print the spec, don't write it")
    args = ap.parse_args()
    print(spec(args.page_id, args.rewrite, args.dry_run))


if __name__ == "__main__":
    main()
