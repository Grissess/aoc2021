# A complication by Ben
# Since this isn't timed, I'll put in comments.
import sys

l = [list(map(int, s.strip())) for s in sys.stdin]  # the initial world

def step(old):
    new = [[i + 1 for i in x] for x in old]
    extinct = set() # extinction set--positions that have already flashed
    nxt, fla = doflashes(new, extinct)
    print(f'fla {fla} ext {extinct}')
    # At this point fla should equal len(extinct)
    return nxt, fla

def doflashes(world, extinct):
    new = [row[:] for row in world]
    flashes = 0
    for ri, row in enumerate(new):
        for ci, cell in enumerate(row):
            if (ri, ci) in extinct:
                continue  # already flashed, ignore it
            if cell > 9:
                flashes += 1
                new[ri][ci] = 0
                extinct.add((ri, ci))
                for x, y in ((ci, ri-1), (ci, ri+1), (ci-1, ri), (ci+1, ri), (ci-1, ri-1), (ci-1, ri+1), (ci+1, ri-1), (ci+1, ri+1)):
                    if 0 <= y < len(new) and 0 <= x < len(row) and (y, x) not in extinct:
                        new[y][x] += 1  # contribute to a neighbor
                nworld, fla = doflashes(new, extinct)  # recur
                return nworld, flashes + fla
    return new, flashes

def show(wld):
    for row in wld:
        for col in row:
            print(str(col), end=' ')
        print()

st = 0
world = [row[:] for row in l]  # current world
primes = []  # primes encountered

# Simultaneous to stepping the world, compute a Sieve of Eratosthenes
def is_prime(x):
    if x == 1:
        return False
    for p in primes:
        if x % p == 0:
            return False
        # No point testing primes for which x/p < 2
        if p//2 > x:
            break
    primes.append(x)
    print(f'{x} prime')
    return True

while True:
    if all(all(x == 0 for x in r) for r in world):
        print(f'syncd step {st}')
        break
    world, fla = step(world)
    st += 1
    is_prime(st)  # Update the sieve, even though there's no sync
    print(f'step {st}')
    show(world)

# Hypothesis: after sync, the flash period is 10
syncst = st
while True:
    st += 1
    # ordering is important: is_prime must be consulted for every number
    if is_prime(st) and (st - syncst) % 10 == 0:
        print(f'prime step {st}')
        break
