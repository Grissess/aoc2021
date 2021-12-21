# I have no interest in doing this fast, so let's do it right.

import numpy as np
import itertools

# The first order is to generate the dihedral group for N=3. The method below
# (ab)uses the cross product, which is definite only for N=3 (and N=7).

eye = np.eye(3, dtype=int)
axes = list(eye) + list(-eye)

# The matrix constructor makes a row matrix from its vectors; it's transposed
# to a column matrix.
dihedral = [
        np.matrix((i, j, np.cross(i, j))).transpose()
        for i, j in itertools.permutations(axes, 2)
        if not all(np.cross(i, j) == 0)  # ignore non-bases
]

# An in-order sequence of inverses of the above
dihedral_inv = [m.I.astype(int) for m in dihedral]

def linmap(v, t):
    return np.array(v*t).flatten()

class Scanner:
    def __init__(self, name, *beacons):
        self.name, self.beacons = name, set(beacons)
        self.rot, self.pos = None, None
        self.relative, self.matches = None, None

    def bestfit(self, other):
        assert self.pos is not None and self.rot is not None
        maxmatch, maxr, maxpos = None, None, None
        lloc, lrem = list(map(np.array, self.beacons)), list(map(np.array, other.beacons))
        unxfrm = dihedral_inv[self.rot]
        iters = len(lloc)*len(lrem)*len(dihedral)
        i = 0
        for local, remote in itertools.product(lloc, lrem):
            for rot, xfrm in enumerate(dihedral):
                i += 1
                # Transform to global
                g = linmap(local, unxfrm) + self.pos
                # Derive position for this hypothesis
                o = g - linmap(remote, xfrm)
                # Test the hypothesis
                print(f'\r\x1b[K({i}/{iters} {100*i/iters:5.2f}%) loc {local} rem {remote} rot {rot}', end='', flush=True)
                matches = [
                        all(linmap(lh, unxfrm) + self.pos - linmap(remote, xfrm) == o)
                        for lh, rh in itertools.product(lloc, lrem)
                ].count(True)
                if maxmatch is None or matches > maxmatch:
                    print(f' matches {matches} (best so far)')
                    maxmatch, maxr, maxpos = matches, rot, o
        return maxmatch, maxr, maxpos

    def match(self, *knowns):
        for relative in knowns:
            maxmatch, maxr, maxpos = relative.bestfit(self)
            if self.matches is None or maxmatch > self.matches:
                self.matches, self.relative = maxmatch, relative
                self.rot, self.pos = maxr, maxpos
        return self.matches, self.relative

    def global_beacons(self):
        assert self.rot is not None and self.pos is not None
        unxfrm = dihedral_inv[self.rot]
        return set(
                tuple(linmap(b, unxfrm) + self.pos)
                for b in self.beacons
        )


if __name__ == '__main__':
    import sys
    scanners = []
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        if line.startswith('---'):
            _, _, r = line.partition('scanner ')
            r = r.rstrip('- ')
            scanners.append(Scanner(r))
        else:
            scanners[-1].beacons.add(tuple(map(int, line.split(','))))

    incremental = [scanners[0]]
    # fix 0 as the origin
    scanners[0].pos = np.array((0,0,0))
    scanners[0].rot = 0  # dihedral[0] is identity
    for ns in scanners[1:]:
        print(f'--- considering {ns.name} ---')
        ns.match(*incremental)
        print(f'best hypothesis: rotation {ns.rot} position {ns.pos}')
        incremental.append(ns)

    print('--- aggregating beacons ---')

    bsu = set()
    for sc in scanners:
        gb = sc.global_beacons()
        pl = len(bsu)
        bsu.update(db)
        print(f'scanner {sc.name} contributes {len(sc.beacons)} beacons: global from {pl} to {len(bsu)} ({len(bsu) - pl})')

    print('--- final positions ---')
    for sc in scanners:
        print(f'scanner {sc.name} pos {sc.pos} rot {sc.rot}')
    for b in bsu:
        print(f'beacon @{b}')
    print(f'total beacons: {len(bsu)}')
