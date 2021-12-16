import functools, operator
d = {c: int(c, 16) for c in '0123456789ABCDEF'}
REST = object()
WHERE = object()
def bmunch(s):
    x = None
    b = 0
    ba = 0
    tb = 0
    while True:
        bits = (yield x)
        print(f'bits {bits} avail {ba} where {tb} rest {s}')
        if bits is WHERE:
            x = tb
            continue
        elif bits is REST:
            x = (b<<(len(s)*4))|int(s, 16)
            s=''
            continue
        tb += bits
        while bits > ba:
            print(f'fill {bits} <= {ba}')
            b = (b<<4) | d[s[0]]
            ba += 4
            s = s[1:]
            print(f'rest {s}')
        ba -= bits
        x = b>>ba
        b ^= x<<ba
        print(f'x {x}, b {b}')
    yield x

def pkt(s):
    bm = bmunch(s)
    bm.send(None)
    return p_top(bm)

indent='-- '
def p_top(bm, lv=0):
    v = bm.send(3)
    t = bm.send(3)
    print(f'{indent*lv}-- top {v}, {t}')
    if t == 4:
        return v, t, p_lit(bm, lv+1)
    else:
        tlid = bm.send(1)
        l = bm.send(11 if tlid else 15)
        if tlid == 0:
            start = bm.send(WHERE)
            end = start + l
            print(f'{indent*lv}-- top: sub start {start} end {end} l {l}')
            r = []
            while bm.send(WHERE) < end:
                r.append(p_top(bm, lv+1))
            assert bm.send(WHERE) == end
            return v, t, r
        else:
            print(f'{indent*lv}-- top: sub pkts {l}')
            return v, t, [p_top(bm, lv+1) for i in range(l)]

def p_lit(bm, lv=0):
    print('{indent*lv}-- lit')
    r = 0
    while True:
        term = bm.send(1)
        r = (r<<4) | bm.send(4)
        if term == 0:
            print(f'{indent*lv}-- lit={r}')
            return r

def walk(s):
    for ver, tp, val in s:
        yield ver, tp, val
        try:
            iter(val)
        except TypeError:
            pass
        else:
            yield from walk(val)

def eval(ver, tp, val):
    if tp == 0:
        return sum(eval(*x) for x in val)
    elif tp == 1:
        return functools.reduce(operator.mul, (eval(*x) for x in val), 1)
    elif tp == 2:
        return min(eval(*x) for x in val)
    elif tp == 3:
        return max(eval(*x) for x in val)
    elif tp == 4:
        return val
    elif tp == 5:
        return 1 if eval(*val[0]) > eval(*val[1]) else 0
    elif tp == 6:
        return 1 if eval(*val[0]) < eval(*val[1]) else 0
    elif tp == 7:
        return 1 if eval(*val[0]) == eval(*val[1]) else 0

p = pkt(input('packet:'))
print(p)
vertot = sum(ver for ver, tp, val in walk([p]))
print(f'tot {vertot}')
print(f'val {eval(*p)}')
