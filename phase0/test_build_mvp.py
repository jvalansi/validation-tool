from build_mvp import parse_result, summary

r = parse_result('Done, deployed.\n{"status": "built", "url": "https://x.javolabs.com", "repo": "jvalansi/x", '
                 '"needs": ["RentCast: rent comps, $74/mo"], "note": "rent verdicts"}')
assert r["status"] == "built" and r["url"] == "https://x.javolabs.com"
assert summary(r).endswith("built: rent verdicts | needs: RentCast: rent comps, $74/mo")
assert parse_result('Used {"status": "x"} earlier.\n{ "status": "skipped", "note": "hardware"}')["status"] == "skipped"
assert parse_result("crashed")["status"] == "failed"
assert parse_result('{"status": "done"}')["status"] == "failed"
print("ok")
