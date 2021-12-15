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

def step(s, i, rul):
    n = {}
    acc = []
    for pr in i:
        ins = rul.get(pr)
        c = i[pr]
        if ins is None:
            if pr not in n: n[pr] = 0
            n[pr] += c
            continue
        l, r = pr
        ls, rs = l+ins, ins+r
        if ls not in n: n[ls] = 0
        n[ls] += c
        if rs not in n: n[rs] = 0
        n[rs] += c
        if 'CO' in (ls, rs):
            print(f'{(ls, rs)}: produced by pair {pr} in amount {c}')
    l = None
    for idx, c in enumerate(s):
        if l is not None:
            ins = rul.get(l+c)
            if ins is not None:
                acc.append(ins)
        acc.append(c)
        if acc[-2:] == ['C', 'O']:
            print(f'CO: produced by pair {l}{c} at index {idx} in {len(acc)}')
        l = c
    return ''.join(acc), n

def mkc(s):
    d = {}
    for pr in zip(s, s[1:]):
        pr = ''.join(pr)
        if pr not in d: d[pr] = 0
        d[pr] += 1
    return d

state1 = init
state2 = mkc(init)
print(f'init: {state1} => {state2}')

for st in range(10):
    state1, state2 = step(state1, state2, rules)
    print(f'{st+1}: {state2}, {state1[:200]}{"..." if len(state1)>200 else ""}')
    scnt = mkc(state1)
    if scnt != state2:
        print('COUNTS DIFFER')
        print('key: pair state, counted')
        for k in set(state2.keys())|set(scnt.keys()):
            print(f'{k}: {state2.get(k, "not present")}, {scnt.get(k, "not present")} {"!" if state2.get(k) != scnt.get(k) else ""}')
        exit()

senset = set((SENTINEL,))
elems1 = set(state1) - senset
elems2 = set(a[0] for a in state2) | set(a[1] for a in state2) - senset
print(f'elems: {elems1}, {elems2} ({elems1 ^ elems2})')
cnts1 = {c: state1.count(c) for c in elems1}
cnts2 = {e: max(sum(state2[i] for i in state2 if e == i[x]) for x in range(2)) for e in elems2}
print(cnts1)
print(cnts2)
for elem in elems1|elems2:
    print(f'{elem}: {cnts1.get(elem)}, {cnts2.get(elem)} {"!" if cnts1.get(elem) != cnts2.get(elem) else ""}')
for cntss in (cnts1, cnts2):
    maxe, mine = max(cntss.items(), key=lambda p: p[1]), min(cntss.items(), key=lambda p: p[1])
    print(f'max, min, diff: {maxe}, {mine}, {maxe[1]-mine[1]}')
