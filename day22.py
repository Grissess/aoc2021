import sys, collections, bisect, itertools, functools, operator
cmds = []
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    cmd, _, co = line.partition(' ')
    cmps = [
            (lambda r: (lambda n, _, x: (int(n),int(x)))(*r.partition('..')))(i.partition('=')[2])
            for i in co.split(',')
    ]
    cmds.append((True if cmd == 'on' else False, cmps))
dims = len(cmds[0][1])
sortitions = [set() for _ in range(dims)]
rules = collections.defaultdict(list)
for dim in range(dims):
    for cmd,cmps in cmds:
        sortitions[dim].update({cmps[dim][0], cmps[dim][1]+1})  # range is inclusive
sortitions = [sorted(i) for i in sortitions]
print('sortitions:')
for x in sortitions: print(x)
def all_ids(): yield from itertools.product(*(range(len(x)-1) for x in sortitions))
idl = functools.reduce(operator.mul, (len(i)-1 for i in sortitions), 1)
print(f'{idl} indices')
#points = {
#        idx: (tuple(s[i] for s,i in zip(sortitions, idx)), tuple(s[i+1] for s,i in zip(sortitions, idx)))
#        for idx in all_ids()
#}
point = lambda idx: (tuple(s[i] for s,i in zip(sortitions, idx)), tuple(s[i+1] for s,i in zip(sortitions, idx)))
#volumes = {
#        idx: functools.reduce(operator.mul, map(lambda p: p[1]-p[0], zip(points[idx][0], points[idx][1])), 1)
#        for idx in all_ids()
#}
volume = lambda idx: functools.reduce(operator.mul, map(lambda p: p[1]-p[0], zip(*point(idx))), 1)
#print(cmds)
#print(sortitions)
#print(all_ids())
#print(points)
#print(volumes)
seq=lambda *args: args[-1]
for st, pr in enumerate(cmds):
    cmd,cmps=pr
    #print(f'cmds: {it}/{itrs} {100*it/itrs:5.2f}%', end=' ')
    axl, axh = zip(*cmps)
    lows = []
    highs = []
    for axis in range(dims):
        i1, i2 = axl[axis], axh[axis]
        s = sortitions[axis]
        lows.append(bisect.bisect_left(s, i1))
        highs.append(min((bisect.bisect_left(s, i2), len(s)-2)))
    print(f'axl,axh {axl},{axh} indexr {lows},{highs}')
    rules[(tuple(lows), tuple(highs))].append((st,cmd))
    #for idx in itertools.product(*(range(l, h+1) for l,h in zip(lows,highs))):
        #if all(seq(print(f'{n}>={i1} and {x}<={i2+1} == {n>=i1 and x<=i2+1}'), n>=i1 and x<=i2+1) for n,x,i1,i2 in zip(points[idx][0],points[idx][1],axl,axh)):
        #if all(n>=i1 and x<=i2+1 for n,x,i1,i2 in zip(*(point(idx) + (axl,axh)))):
            #rules[idx] = cmd
print(f'{len(rules)} rules to consider')
onvol = 0
for it,idx in enumerate(all_ids()):
    if it%5000==0: print(f'all indices: {it}/{idl} {100*it/idl:6.3f}%')
    hits = [v for k,v in rules.items() if all(n>=i1 and x<=i2+1 for n,x,i1,i2 in zip(*(k+point(idx))))]
    hits = list(itertools.chain.from_iterable(hits))
    if not hits: continue
    try:
        fist = max(hits, key=lambda p: p[0])[1]
    except IndexError:
        print(f'FAILED! hits {hits}')
        raise
#for idx in all_ids():
    #print(f'cube {idx}:{points[idx]}: {rules[idx] if idx in rules else []}')  # don't make a new list
    if fist:
        onvol += volume(idx)
print(f'tot {onvol}')
