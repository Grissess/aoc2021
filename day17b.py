line = input('area:')
_, _, coords = line.partition(':')
xp, _, yp = coords.strip().partition(', ')
def procpart(x):
    _, _, mm = x.partition('=')
    mn, _, mx = mm.partition('..')
    return int(mn), int(mx)
xb, yb = map(procpart, (xp, yp))

print('ranging x...')
ix = 0
tx = 0
xn, xx = xb
while tx < xn:
    ix += 1
    tx += ix
if tx > xx:
    print(f'no solution, ix {ix} tx {tx} xx {xx}')
    exit()
print(f'candidate id {ix} tx {tx} xn {xn} xx {xx}')

def trinum():
    i = 1
    x = 0
    while True:
        yield x
        x += i
        i += 1

print('ranging y...')
yn, yx = yb
lhiy = None
try:
    for iy in range(999999999):
        print(f'iy={iy}:', end=' ')
        s, y = 0, 0
        stop = False
        for tri in trinum():
            s += 1
            py = y
            y = s*iy - tri
            if y < yn:
                if py >= 0:
                    print('(too fast, stop)', end=' ')
                    stop = True
                print(f'missed under: {y} < {yn}, {py}')
                break
            if yn <= y <= yx and s >= ix:
                if lhiy != iy:
                    print('HIT!')
                    lhiy = iy
                    break
        if stop:
            break
except KeyboardInterrupt:
    print('Aborting!')
print(f'last hit iy: {lhiy}')

def traj(ix, iy):
    vx, vy = ix, iy
    x, y = 0, 0
    while True:
        if x > xx or y < yn:
            return
        yield vx, vy, x, y
        x += vx
        y += vy
        vy -= 1
        if vx > 0: vx -= 1

print('determining all hits...')
hits = 0
for ix in range(xx+1):
    for iy in range(lhiy, yn-1, -1):
        for vx, vy, x, y in traj(ix, iy):
            if xn <= x <= xx and yn <= y <= yx:
                print(f'{ix},{iy}')
                hits += 1
                break
print(f'hits {hits}')
