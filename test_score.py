from analyze import score

assert score(0, 0, 1.0) == 0.0
assert score(10, 0, 0.5) == 5.0
assert score(10, 10, 0.5) == 10.0          # every item shows paying → doubles
assert score(20, 0, 0.5) > score(10, 5, 0.5)  # frequency still dominates a small pay share
print("ok")
