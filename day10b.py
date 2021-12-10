import sys
lines = [l.strip() for l in sys.stdin if l.strip()]
delims = {'(': ')', '[': ']', '{': '}', '<': '>'}
closes = set(delims.values())
scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
clscores = {')': 1, ']': 2, '}': 3, '>': 4}
BAD, INCOMP = object(), object()
def parse(x):
    stk = []
    for c in x:
        print(f'c {c} stk {stk}')
        if c in delims:
            stk.append(c)
        elif c in closes:
            op = stk.pop()
            cld = delims[op]
            if c != cld:
                return BAD, op, c
        else:
            raise ValueError(c)
    if stk:
        return INCOMP, stk
    return True

scores = []
for i, l in enumerate(lines):
    print(i, end=' ')
    res = parse(l)
    if res[0] is True:
        print('OK')
    elif res[0] is BAD:
        _, op, cl = res
        print(f'Bad: opened {op}, closed {cl}')
    elif res[0] is INCOMP:
        _, stk = res
        sc = 0
        for c in reversed(stk):
            sc = 5*sc + clscores[delims[c]]
        scores.append(sc)
        print(f'Incomp: needs {stk}, score {sc}')
    else:
        assert False
scores.sort()
print(f'Scores: {scores}')
mid = scores[len(scores)//2]
print(f'Mid: {mid}')
