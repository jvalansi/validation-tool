from analyze import score
from sweep import rank

assert score(0, 0, 1.0) == 0.0
assert score(10, 0, 0.5) == 5.0
assert score(10, 10, 0.5) == 10.0          # every item shows paying → doubles
assert score(20, 0, 0.5) > score(10, 5, 0.5)  # frequency still dominates a small pay share

# Excluded clusters never rank, however high their score.
top = rank([{"niche": "a", "items": 9, "paying": 9, "ml_fit": 1, "excluded": "hardware"},
            {"niche": "a", "items": 3, "paying": 0, "ml_fit": 1, "excluded": None}])
assert [c["items"] for c in top] == [3], top
# A big niche doesn't outrank a small one on volume alone: 50% of a small niche beats 10% of a big one.
top = rank([{"niche": "big", "items": 100, "paying": 0, "ml_fit": 1, "excluded": None},
            {"niche": "big", "items": 900, "paying": 0, "ml_fit": 0, "excluded": None},
            {"niche": "small", "items": 10, "paying": 0, "ml_fit": 1, "excluded": None},
            {"niche": "small", "items": 10, "paying": 0, "ml_fit": 0, "excluded": None}])
assert top[0]["niche"] == "small", top
print("ok")
