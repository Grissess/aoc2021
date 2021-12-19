COLORS = [f'\x1b[{c}m' for c in ('31', '32', '33', '34', '1;31', '1;32', '1;33', '1;34')]
RESET = '\x1b[m'
def color(i):
    if not COLORS:
        return ''
    return COLORS[i%len(COLORS)]

DEBUG = False
def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

class SPath:
    def __init__(self, *choices):
        self.choices = choices

    @property
    def here(self):
        return not self.choices

    @property
    def left(self):
        return not self.choices[0]

    @property
    def next(self):
        return SPath(*self.choices[1:])

    def __len__(self):
        return len(self.choices)

    def __add__(self, rhs):
        if not isinstance(rhs, SPath):
            return NotImplemented
        return SPath(*(self.choices + rhs.choices))

    def __repr__(self):
        items = (f'{color(idx)}{"R" if v else "L"}{RESET}' for idx, v in enumerate(self.choices))
        return f'SPath({", ".join(items)})'

SPath.EMPTY = SPath()
SPath.LEFT = SPath(False)
SPath.RIGHT = SPath(True)

class SNum:
    DEPTH, LIMIT = 4, 9
    def __init__(self, l, r=None):
        self.l, self.r = l, r

    @classmethod
    def from_(cls, l):
        if isinstance(l, int):
            return cls(l)
        if len(l) != 2:
            raise ValueError(l)
        return SNum(*map(cls.from_, l))

    def pretty(self, lv=0):
        if self.leaf:
            return repr(self.l)
        return f'{color(lv)}[{self.l.pretty(lv+1)}{color(lv)},{self.r.pretty(lv+1)}{color(lv)}]{RESET}'

    def __repr__(self):
        return self.pretty()

    #def __repr__(self):
    #    if self.leaf:
    #        return repr(self.l)
    #    return repr([self.l, self.r])

    @property
    def leaf(self):
        return self.r is None

    def __add__(self, rhs):
        if not isinstance(rhs, SNum):
            return NotImplemented
        return SNum(self, rhs)

    def __getitem__(self, path):
        if path.here:
            return self
        if self.leaf:
            raise IndexError(self, path)
        return (self.l if path.left else self.r)[path.next]

    def with_(self, path, value, top=True):
        if path.here:
            res = value
        else:
            if self.leaf:
                raise IndexError(self, path)
            if path.left:
                res = SNum(self.l.with_(path.next, value, False), self.r)
            else:
                res = SNum(self.l, self.r.with_(path.next, value, False))
        if top:
            dprint(f'{self} .with({path}, {value}) => {res}')
        return res

    def removed(self, path):
        if self.leaf:
            raise IndexError(self, path)
        if len(path)==1:
            return (self.r if path.left else self.l)
        return (self.l if path.left else self.r).removed(path.next)

    def preorder(self):
        yield SPath.EMPTY, self
        if self.leaf:
            return
        try:
            for p, v in self.l.preorder():
                yield SPath.LEFT + p, v
            for p, v in self.r.preorder():
                yield SPath.RIGHT + p, v
        except AttributeError:
            raise ValueError(f'{self} has non-snum: {type(self.l)}({self.l}), {type(self.r)}({self.r})')

    @property
    def reachable(self):
        return set(v for p, v in self.preorder())

    def exploded(self, depth=None):
        if depth is None: depth = self.DEPTH
        po = self.preorder()
        last_leaf_path, last_leaf_val = None, None
        while True:
            try:
                p, v = next(po)
            except StopIteration:
                return self
            if len(p) >= depth and not v.leaf:
                dprint(f'split at {p}, {v}')
                # This is only correct if the depth only ever increases by one--these must be leaves
                assert v.l.leaf and v.r.leaf, f'{v} @ {p} has non-leaf children'
                lv, rv = v.l.l, v.r.l
                # Pay close attention to the operation order here!
                s = self
                if last_leaf_path is not None:
                    dprint(f'... last leaf {last_leaf_path},{last_leaf_val} with {lv}')
                    s = s.with_(last_leaf_path, SNum(last_leaf_val.l + lv))
                next_leaf_path, next_leaf_val = None, None
                ignore = v.reachable
                while True:
                    np, nv = next(po, (None, None))
                    if np is None: break
                    if nv in ignore: continue
                    if nv.leaf:
                        next_leaf_path, next_leaf_val = np, nv
                        break
                if next_leaf_path is not None:
                    dprint(f'... next leaf {next_leaf_path},{next_leaf_val} with {rv}')
                    s = s.with_(next_leaf_path, SNum(next_leaf_val.l + rv))
                return s.with_(p, SNum.ZERO).exploded(depth)
            if v.leaf:
                last_leaf_path, last_leaf_val = p, v

    def split(self, limit=None, depth=None):
        if limit is None: limit = self.LIMIT
        for p, v in self.preorder():
            if v.leaf and v.l > limit:
                l = v.l // 2
                r = v.l - l
                return self.with_(p, SNum(SNum(l), SNum(r))).exploded(depth).split(limit, depth)
        return self

    @property
    def reduced(self):
        return self.exploded().split()

    @property
    def magnitude(self):
        if self.leaf:
            return self.l
        return 3*self.l.magnitude + 2*self.r.magnitude

SNum.ZERO = SNum(0)
