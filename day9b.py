import sys, functools, operator
mp = [list(map(int,l.strip())) for l in sys.stdin]
def is_low(x, y):
    q = mp[y][x]
    test = []
    if x > 0:
        test.append(mp[y][x-1])
    if x < len(mp[y])-1:
        test.append(mp[y][x+1])
    if y > 0:
        test.append(mp[y-1][x])
    if y < len(mp)-1:
        test.append(mp[y+1][x])
    return q < min(test)
def floodfill(x,y,lim=9):
    members = set()
    opn=[(x,y)]
    while opn:
        x,y=opn.pop(0)
        if mp[y][x]==lim: continue
        if (x,y) in members: continue
        members.add((x,y))
        if x>0: opn.append((x-1,y))
        if x<len(mp[y])-1: opn.append((x+1,y))
        if y>0: opn.append((x,y-1))
        if y<len(mp)-1: opn.append((x,y+1))
    return list(members)
seeds=[]
for y in range(len(mp)):
    for x in range(len(mp[y])):
        if is_low(x,y):
            seeds.append((x,y))
print(seeds)
basins=[floodfill(x,y) for x,y in seeds]
basins.sort(key=lambda b: len(b), reverse=True)
top3=basins[:3]
print(list(map(len, top3)), functools.reduce(operator.mul, map(len, top3)))
