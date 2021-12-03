import sys
values = list(map(int, sys.stdin))
signum = lambda x: 1 if x > 0 else -1 if x < 0 else 0
print([signum(y-x) for x, y in zip(values, values[1:])].count(1))
