import numpy as np, sys
pop = np.array([0]*9)
for f in (int(x) for x in input('fish:').split(',')):
    pop[f] += 1
fbm = np.concatenate((np.matrix([[0, 0, 0, 0, 0, 0, 1, 0, 1]]),np.identity(9,int)[:8]))
fbm **= int(input('steps:'))
print(fbm)
out = pop * fbm
print(out, out.sum())
