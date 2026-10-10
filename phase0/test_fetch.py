from fetch import _upwork_item

job = _upwork_item({"href": "https://www.upwork.com/freelance-jobs/apply/Shopify-Data-Entry-Specialist_~022105120111807408864/",
                    "title": "Shopify Data Entry Specialist - Freelance Job in ... - Upwork", "body": "We need a reliable freelancer"})
assert job["id"] == "uw:022105120111807408864" and job["title"] == "Shopify Data Entry Specialist", job
assert _upwork_item({"href": "https://www.upwork.com/freelance-jobs/bookkeeping/", "title": "x", "body": "Browse 2,087 open jobs"}) is None
assert _upwork_item({"href": "https://www.upwork.com/freelance-jobs/apply/X_~123/", "title": "x",
                     "body": "Find & apply for freelance jobs on Upwork"}) is None
print("ok")

from fetch import _freelancer_item
fl = _freelancer_item({"id": 1, "seo_url": "x/Y", "time_submitted": 0, "type": "fixed", "title": "T", "description": "D",
                       "currency": {"code": "USD"}, "budget": {"minimum": 30.0, "maximum": 250.0}, "bid_stats": {"bid_count": 54}})
assert fl["body"] == "Budget 30-250 USD fixed, 54 bids. D" and fl["engagement"] == 54 and fl["created"] == "1970-01-01", fl
print("ok")

from fetch import transcript_chunks
text = "we talk about the weather " * 100 + "honestly reconciling by hand is so tedious " + "nice day " * 100
kept = transcript_chunks(text)
assert len(kept) == 1 and "tedious" in kept[0][1], kept
print("ok")

from fetch import transcript_text
srt = "1\n00:00:01,000 --> 00:00:03,000\nreconciling is tedious\n\n2\n00:00:03,500 --> 00:00:05,000\n<v Host>every month</v>\n"
assert transcript_text("WEBVTT\n\n" + srt) == "reconciling is tedious every month", transcript_text(srt)
assert transcript_text('{"segments": [{"body": "a"}, {"body": "b"}]}') == "a b"
print("ok")
