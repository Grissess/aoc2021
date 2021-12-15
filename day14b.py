import sys

SENTINEL='_' # must not be in input state
init = input('start:')+SENTINEL
sys.stdin.readline() # blank
rules = {}
for l in sys.stdin:
    l = l.strip()
    if not l: continue
    lhs, _, rhs = l.partition(' -> ')
    rules[lhs] = rhs

def step(i, rul):
    n = {}
    for pr in i:
        ins = rul.get(pr)
        c = i[pr]
        if ins is None:
            if pr not in n: n[pr] = 0
            n[pr] += c
            continue
        l, r = pr
        if l+ins not in n: n[l+ins] = 0
        n[l+ins] += c
        if ins+r not in n: n[ins+r] = 0
        n[ins+r] += c
    return n

state = {}
for pr in zip(init, init[1:]):
    s = ''.join(pr)
    if s not in state: state[s] = 0
    state[s] += 1

for st in range(40):
    state = step(state, rules)
    print(f'{st+1}: {state}')

senset = set((SENTINEL,))
elems = set(a[0] for a in state) | set(a[1] for a in state) - senset
print(f'elems: {elems}')
cnts = {e: max(sum(state[i] for i in state if e == i[x]) for x in range(2)) for e in elems}
maxe, mine = max(cnts.items(), key=lambda p: p[1]), min(cnts.items(), key=lambda p: p[1])
print(f'max, min, diff: {maxe}, {mine}, {maxe[1]-mine[1]}')
