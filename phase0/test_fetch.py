from fetch import _upwork_item

job = _upwork_item({"href": "https://www.upwork.com/freelance-jobs/apply/Shopify-Data-Entry-Specialist_~022105120111807408864/",
                    "title": "Shopify Data Entry Specialist - Freelance Job in ... - Upwork", "body": "We need a reliable freelancer"})
assert job["id"] == "uw:022105120111807408864" and job["title"] == "Shopify Data Entry Specialist", job
assert _upwork_item({"href": "https://www.upwork.com/freelance-jobs/bookkeeping/", "title": "x", "body": "Browse 2,087 open jobs"}) is None
assert _upwork_item({"href": "https://www.upwork.com/freelance-jobs/apply/X_~123/", "title": "x",
                     "body": "Find & apply for freelance jobs on Upwork"}) is None
print("ok")
