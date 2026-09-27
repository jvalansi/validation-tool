from analyze import score
from sweep import rank

assert score(0, 0, 1.0) == 0.0
assert score(10, 0, 0.5) == 5.0
assert score(10, 10, 0.5) == 10.0          # every item shows paying → doubles
assert score(20, 0, 0.5) > score(10, 5, 0.5)  # frequency still dominates a small pay share

# Excluded clusters never rank, however high their score.
top = rank([{"score": 99, "paying": 9, "excluded": "hardware"}, {"score": 1, "paying": 0, "excluded": None}])
assert [c["score"] for c in top] == [1], top
print("ok")
