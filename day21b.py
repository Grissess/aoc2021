import collections, itertools
a,b = map(int, input('starts(a,b):').split(','))
st = (a,b,True,0,0)
board = 10
def remap(x):
    return (x-1)%board + 1
# state: (pa,pb,a?,sa,sb)
outcomes = collections.defaultdict(int)
opn = set()
# collect dist
mvs=collections.defaultdict(int)
for a,b,c in itertools.product(*([[1,2,3]]*3)):
    mvs[sum((a,b,c))]+=1
print(f'dist: {mvs}')
print('simulating...')
# there is 1 way for the game to start
outcomes[st] = 1
opn.add(st)
lim=21
iters = 0
while opn:
    iters += 1
    st = opn.pop()
    sc = outcomes[st]
    if iters%1000== 0:
        print(f'{iters}: {st} = {sc} ({len(opn)})')
    for offs,sco in mvs.items():
        a,b,isa,sca,scb = st
        if isa:
            a = remap(a+offs)
            sca += a
        else:
            b = remap(b+offs)
            scb += b
        isa = not isa
        nst = (a,b,isa,sca,scb)
        outcomes[nst] += sco*sc
        if sca<lim and scb<lim:
            opn.add(nst)
        if sca>=lim and scb>=lim:
            print(f'both won?! {st} -{(offs,sco)}-> {nst}, wtf')
            exit(1)
print(f'aggregating {len(outcomes)} states...')
at, bt = 0, 0
for st,sc in outcomes.items():
    _, _, _, sca, scb = st
    if sca >= lim and scb >= lim:
        print(f'INCONSISTENT: {sca} and {scb} >= {lim} in state {st}')
        exit(1)
    elif sca >= lim:
        at += sc
    elif scb >= lim:
        bt += sc

print('wins:')
print(f'a: {at}')
print(f'b: {bt}')
