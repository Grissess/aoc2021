import sys
mp = [l.strip() for l in sys.stdin]
def is_low(x, y):
    q = int(mp[y][x])
    test = []
    if x > 0:
        test.append(int(mp[y][x-1]))
    if x < len(mp[y])-1:
        test.append(int(mp[y][x+1]))
    if y > 0:
        test.append(int(mp[y-1][x]))
    if y < len(mp)-1:
        test.append(int(mp[y+1][x]))
    return q < min(test)
tot=0
for y in range(len(mp)):
    for x in range(len(mp[y])):
        if is_low(x,y):
            q = int(mp[y][x])
            print(f'low {x},{y}: {q}')
            tot += q+1
print(tot)
