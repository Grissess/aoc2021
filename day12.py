import sys
edges = [(lambda a, _, b: (a,b))(*l.strip().partition('-')) for l in sys.stdin]

vertices = frozenset(a for a,b in edges)|frozenset(b for a,b in edges)
edges = {k: frozenset(a for a,b in edges if b == k) | frozenset(b for a,b in edges if a == k) for k in vertices}
START, END = 'start', 'end'

def visitor(here, small, path=()):
    print(f'here {here} sm {small} pth {path}')
    old_pth = path
    path = path + (here,)
    if here == END:
        #print('is end')
        yield path
    elif here in old_pth and here in small:
        #print('already in path')
        pass
    else:
        #print(f'nv {visitable}')
        for neigh in edges[here]:
            print(f'neigh {neigh}')
            yield from visitor(neigh, small, path)

small = frozenset(v for v in vertices if v == v.lower())
print(vertices)
print(edges)
print(small)
cnt = 0
for pth in visitor(START, small):
    cnt += 1
    print(pth)
print(f'paths {cnt}')
