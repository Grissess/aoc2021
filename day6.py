import sys
fish = [int(x) for x in input('fish:').split(',')]
def step(fish):
    new = []
    for idx, f in enumerate(fish):
        if f == 0:
            fish[idx] = 6
            new.append(8)
        else:
            fish[idx] -= 1
    return fish + new
steps = int(input('steps:'))
for s in range(steps):
    print(s, ':', len(fish))
    fish = step(fish)
print('Final:', len(fish))
