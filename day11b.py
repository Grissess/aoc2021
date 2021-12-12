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

st = 0
world = [row[:] for row in l]
while True:
    if all(all(x == 0 for x in r) for r in world):
        print(f'syncd step {st}')
        break
    world, fla = step(world)
    st += 1
    print(f'step {st}')
    show(world)
