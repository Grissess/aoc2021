import sys

def path(gr, g, s=(0,0), n=((1,0),(0,1),(-1,0),(0,-1))):
    opn = [(s, 0)]
    cls = set()
    back = {}
    costs = {}
    while opn:
        here, cost = opn.pop(0)
        if here == g:
            path = [here]
            cur = here
            while cur != s:
                cur = back[cur]
                path.append(cur)
            path.append(s)
            return list(reversed(path)), cost
        x, y = here
        for nd in n:
            dx, dy = nd
            tx, ty = x+dx, y+dy
            if 0 <= tx < len(gr[0]) and 0 <= ty < len(gr):
                there = (tx, ty)
                nc = gr[ty][tx]
                tc = cost + nc
                if there not in costs or tc < costs[there]:
                    costs[there] = tc
                    back[there] = here
                if there not in cls:
                    opn.append((there, tc))
                    cls.add(there)
        opn.sort(key = lambda p: p[1])
    return None, None

gr = [list(map(int, l.strip())) for l in sys.stdin if l.strip()]
w, h = len(gr[0]), len(gr)
pth, cst = path(gr, (w-1, h-1))
print(f'path {pth}')
print(f'cost {cst}')
