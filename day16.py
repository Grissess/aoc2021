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

class Pkt:
    def __init__(self, ver, tp, lc, l, val):
        self.ver, self.tp, self.lc, self.l, self.val = ver, tp, lc, l, val

    OPTBL = {0: '+', 1: '*', 2: 'min', 3: 'max', 5: '<', 6: '>', 7: '=='}
    def __repr__(self):
        ret = f'<Packet ver={self.ver} tp={self.tp} '
        if self.tp == 4:
            return ret + f'val={self.val}>'
        return ret + f'lc={self.lc} l={self.l}>'

    def __str__(self):
        if self.tp == 4:
            return str(self.val)
        return self.OPTBL[self.tp] + f'({self.lc},{self.l})'

    def walk(self, stk=()):
        yield self, stk
        try:
            iter(self.val)
        except TypeError:
            pass
        else:
            ns = stk + (self,)
            for i in self.val:
                yield from i.walk(ns)

    def eval(self):
        if self.tp == 0:
            return sum(x.eval() for x in self.val)
        elif self.tp == 1:
            return functools.reduce(operator.mul, (x.eval() for x in self.val), 1)
        elif self.tp == 2:
            return min(x.eval() for x in self.val)
        elif self.tp == 3:
            return max(x.eval() for x in self.val)
        elif self.tp == 4:
            return self.val
        elif self.tp == 5:
            return 1 if self.val[0].eval() > self.val[1].eval() else 0
        elif self.tp == 6:
            return 1 if self.val[0].eval() < self.val[1].eval() else 0
        elif self.tp == 7:
            return 1 if self.val[0].eval() == self.val[1].eval() else 0

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
        return Pkt(v, t, 0, 0, p_lit(bm, lv+1))
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
            return Pkt(v, t, tlid, l, r)
        else:
            print(f'{indent*lv}-- top: sub pkts {l}')
            return Pkt(v, t, tlid, l, [p_top(bm, lv+1) for i in range(l)])

def p_lit(bm, lv=0):
    print('{indent*lv}-- lit')
    r = 0
    while True:
        term = bm.send(1)
        r = (r<<4) | bm.send(4)
        if term == 0:
            print(f'{indent*lv}-- lit={r}')
            return r

p = pkt(input('packet:'))
print('structure:')
for pk, st in p.walk():
    print(f'{"  "*len(st)}{pk!s}')
vertot = sum(pk.ver for pk,st in p.walk())
print(f'tot {vertot}')
print(f'val {p.eval()}')
