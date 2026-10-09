from spec import SECTIONS, check, rich, to_blocks

md = "Here it is.\n" + "\n".join(f"### {s}\n- **Key**: see [src](https://x.org/a)" for s in SECTIONS)
assert check(md).startswith("### Customer")
try:
    check(md.replace("### Out of scope", "### Range"))
    assert False, "missing section accepted"
except ValueError as e:
    assert "Out of scope" in str(e)
b = to_blocks("### Input\n- a link\n2. Given x, When y, Then z\nplain")
assert [x["type"] for x in b] == ["heading_3", "bulleted_list_item", "numbered_list_item", "paragraph"]
assert b[2]["numbered_list_item"]["rich_text"][0]["text"]["content"] == "Given x, When y, Then z"
r = rich("**Key**: see [src](https://x.org/a) 2*3")
assert r[0]["annotations"]["bold"] and r[2]["text"]["link"]["url"] == "https://x.org/a"
assert "".join(p["text"]["content"] for p in r) == "Key: see src 2*3"
print("ok")

n = to_blocks("### Scope\n- **In:**\n  - a\n  - b\n- **Out:** c\n### Next\nx")
assert [x["type"] for x in n] == ["heading_3", "bulleted_list_item", "bulleted_list_item", "heading_3", "paragraph"]
assert [k["bulleted_list_item"]["rich_text"][0]["text"]["content"] for k in n[1]["bulleted_list_item"]["children"]] == ["a", "b"]
assert "children" not in n[2]["bulleted_list_item"]
print("ok nested")
