a,b = map(int, input('starts(a,b):').split(','))
board = 10
def remap(x):
    return (x-1)%board + 1
def detdie():
    while True:
        yield from range(1,101)
def diectr(die, cell):
    cell[0] = 0
    for x in die:
        cell[0] += 1
        yield x
def turn(die, s):
    x = remap(sum((s, next(die), next(die), next(die))))
    return x
def game(die, ps, lim=1000):
    ps = list(ps)
    scs = [0]*len(ps)
    rnd = 0
    while True:
        rnd += 1
        for i in range(len(ps)):
            ps[i] = turn(die, ps[i])
            scs[i] += ps[i]
            if scs[i] >= lim: return rnd, ps, scs
rollcell=[0]
die=diectr(detdie(),rollcell)
rnd, ps, scs = game(die, [a,b])
loser = [s for s in scs if s<1000][0]
print(f'final round {rnd} scores {scs} positions {ps} loser {loser} rolls {rollcell[0]} product {rollcell[0]*loser}')
