import sys
inp = [int(x) for x in input('positions:').strip().split(',')]
mx = max(inp)
sod = [(i, sum(abs(x - i) for x in inp)) for i in range(mx+1)]
open('data', 'w').write('\n'.join(f'{x}\t{y}' for x, y in sod)+'\n')
mn, argmin = min(sod, key=lambda p: p[1])
print(mn, argmin)
