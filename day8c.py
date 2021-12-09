import sys, itertools
groups = [(lambda l, _, r: (l.split(), r.split()))(*l.strip().partition('|')) for l in sys.stdin]
patterns = {
        'abcefg': 0,
        'cf': 1,
        'acdeg': 2,
        'acdfg': 3,
        'bcdf': 4,
        'abdfg': 5,
        'abdefg': 6,
        'acf': 7,
        'abcdefg': 8,
        'abcdfg': 9,
}
pk = frozenset(patterns.keys())

def cmp_permute(obs):
    for permute in itertools.permutations('abcdefg'):
        mp = {x: y for x, y in zip('abcdefg', permute)}
        res = [''.join(sorted(mp[x] for x in i)) for i in obs]
        #print(f'{obs} permute {permute} res {res}')
        if set(res) - pk:
            continue
        return mp

runtot = 0
for obs, outs in groups:
    d = cmp_permute(obs)
    digs = [patterns[''.join(sorted(d[x] for x in i))] for i in outs]
    num = int(''.join(map(str, digs)))
    runtot += num
    print(f'obs {obs} map {d} digs {digs} num {num}')
print(runtot)
