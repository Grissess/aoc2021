import sys
inp = [int(x) for x in input('positions:').strip().split(',')]
print((sum(inp) + 1) / len(inp))
