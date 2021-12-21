import sys
mapping = input('filter:').strip()
if len(mapping) != 512:
    print(f'check inputs! len map = {len(mapping)}')
    exit(1)
input()  # blank
pts = set()
for row, line in enumerate(sys.stdin):
    line = line.strip()
    for col, ch in enumerate(line):
        if ch == '#':
            pts.add((col, row))
def bounds(q):
    xs, ys = {x for x,y in q}, {y for x,y in q}
    xn, xx, yn, yx = min(xs), max(xs), min(ys), max(ys)
    return xn, xx, yn, yx
def apply(q, m, bc=False, sl=1):
    newpts = set()
    xn, xx, yn, yx = bounds(q)
    bits = list(reversed([2**i for i in range(9)]))
    newbc = m[511 if bc else 0] == '#'
    for x in range(xn-sl, xx+sl+1):
        for y in range(yn-sl, yx+sl+1):
            neighs = [(x+dx,y+dy) for dy in (-1,0,1) for dx in (-1,0,1)]
            idx = sum(bits[i] for i, n in enumerate(neighs) if n in q or (not (xn<=n[0]<=xx and yn<=n[1]<=yx)) and bc)
            if m[idx] == '#':
                newpts.add((x,y))
    return newpts, newbc
def show(q):
    xn, xx, yn, yx = bounds(q)
    for y in range(yn, yx+1):
        for x in range(xn, xx+1):
            print('#' if (x,y) in q else '.', end='')
        print()
bc = False
for stp in range(50):
    print(f'step {stp} lit {len(pts)} bc {bc}')
    #show(pts)
    pts, bc = apply(pts, mapping, bc, sl=3)
print(f'final lit {len(pts)}')
#show(pts)
