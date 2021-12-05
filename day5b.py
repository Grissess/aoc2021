import sys
plot = {}
minx, maxx, miny, maxy = 0, 0, 0, 0
failed = 0
for line in sys.stdin:
    a, _, b = line.strip().partition(' -> ')
    ax, _, ay = a.partition(',')
    bx, _, by = b.partition(',')
    ax, ay, bx, by = map(int, (ax, ay, bx, by))
    lx, hx, ly, hy = min(ax, bx), max(ax, bx), min(ay, by), max(ay, by)
    minx, maxx, miny, maxy = min(minx, lx), max(maxx, hx), min(miny, ly), max(maxy, hy)
    if lx == hx or ly == hy:
        for x in range(lx, hx+1):
            for y in range(ly, hy+1):
                plot[(x, y)] = plot.get((x, y), 0) + 1
    elif hx - lx == hy - ly:
        sy, sn = (ly, 1) if (lx,ly)==(ax,ay) or (lx,ly)==(bx,by) else (hy, -1)
        for i in range(hx - lx + 1):
            p = (lx+i, sy+sn*i)
            plot[p] = plot.get(p, 0) + 1
    else:
        failed += 1

for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
        print(plot.get((x, y), 0), end=' ')
    print()

mx = max(plot.values())
ovl = sum(1 for x in plot.values() if x > 1)
print(failed, mx, ovl)
