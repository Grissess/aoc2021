import sys

init = input('start:')
sys.stdin.readline() # blank
rules = {}
for l in sys.stdin:
    l = l.strip()
    if not l: continue
    lhs, _, rhs = l.partition(' -> ')
    rules[lhs] = rhs

def step(i, r):
    acc = []
    l = None
    for c in i:
        if l is not None:
            ins = r[l+c]
            acc.append(ins)
        acc.append(c)
        l = c
    return ''.join(acc)

state = init
for st in range(10):
    state = step(state, rules)
    if len(state)>200:
        print(f'{st+1}: {state[:200]}...')
    else:
        print(f'{st+1}: {state}')

print(f'final: {state}')
elems = set(state)
print(f'elems: {elems}')
cnts = [state.count(e) for e in elems]
maxe, mine = max(cnts), min(cnts)
print(f'max, min, diff: {maxe}, {mine}, {maxe-mine}')
