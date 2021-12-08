import sys
groups = [(lambda l, _, r: (l.split(), r.split()))(*l.strip().partition('|')) for l in sys.stdin]
print(sum(sum(1 for grp in outs if len(grp) in (2,3,4,7)) for obs, outs in groups))
