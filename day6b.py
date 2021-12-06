import sys
fc = {x: 0 for x in range(9)}
fish = [int(x) for x in input('fish:').split(',')]
for f in fish:
    fc[f] += 1
def step(fc):
    nfc = {x: 0 for x in range(9)}
    for k in fc:
        if k == 0:
            nfc[6] += fc[k]
            nfc[8] += fc[k]
        else:
            nfc[k-1] += fc[k]
    return nfc
steps = int(input('steps:'))
for s in range(steps):
    print(s, ':', fc, sum(fc.values()))
    fc = step(fc)
print('Final:', fc, sum(fc.values()))
