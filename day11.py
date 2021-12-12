import sys
l = [list(map(int, s.strip())) for s in sys.stdin]
def step(old):
    new = [[i + 1 for i in x] for x in old]
    extinct = set()
    nxt, fla = doflashes(new, extinct)
    print(f'fla {fla} ext {extinct}')
    return nxt, fla
def doflashes(world, extinct):
    new = [row[:] for row in world]
    flashes = 0
    for ri, row in enumerate(new):
        for ci, cell in enumerate(row):
            if (ri, ci) in extinct:
                continue
            if cell > 9:
                flashes += 1
                new[ri][ci] = 0
                extinct.add((ri, ci))
                for x, y in ((ci, ri-1), (ci, ri+1), (ci-1, ri), (ci+1, ri), (ci-1, ri-1), (ci-1, ri+1), (ci+1, ri-1), (ci+1, ri+1)):
                    if 0 <= y < len(new) and 0 <= x < len(row) and (y, x) not in extinct:
                        new[y][x] += 1
                nworld, fla = doflashes(new, extinct)
                return nworld, flashes + fla
    return new, flashes
def show(wld):
    for row in wld:
        for col in row:
            print(str(col), end=' ')
        print()

tot = 0
world = [row[:] for row in l]
for st in range(100):
    world, fla = step(world)
    tot += fla
    print(f'step {st+1} flashes {tot}')
    show(world)
