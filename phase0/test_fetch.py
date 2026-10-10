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
