import sys

dotpos = []
while True:
    dot = input('dot (blank to end):').strip()
    if not dot:
        break
    dx, _, dy = dot.partition(',')
    dx, dy = int(dx), int(dy)
    dotpos.append((dx, dy))

folds = []
for l in sys.stdin:
    l = l.strip()
    if not l.startswith('fold along '):
        break
    _, _, lw = l.rpartition(' ')
    ax, _, v  = lw.partition('=')
    folds.append((ax, int(v)))

mxx, mxy = max(x for x,y in dotpos), max(y for x,y in dotpos)
w, h = mxx + 1, mxy + 1
s = [[False] * w for _ in range(h)]

def dotcnt():
    return sum(r.count(True) for r in s)

def rsz():
    global s
    del s[h:]
    for i in range(h):
        del s[i][w:]

def fld(ax,v):
    global w, h
    m = w if ax=='x' else h
    for i in range(1,m):
        if v+i>=m: break
        if ax=='x':
            for y in range(h):
                s[y][v-i] = s[y][v-i] or s[y][v+i]
        else:
            for x in range(w):
                s[v-i][x] = s[v-i][x] or s[v+i][x]
    if ax=='x':
        w=v
    else:
        h=v
    rsz()

def shw():
    print(f'W{w}, H{h}')
    for y in range(h):
        for x in range(w):
            print('#' if s[y][x] else '.', end='')
        print()

for x,y in dotpos:
    s[y][x] = True

print('dcpre', dotcnt())
#shw()
for fold in folds:
    fld(*fold)
shw()
print('dcpost', dotcnt())
