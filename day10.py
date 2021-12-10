import sys
lines = [l.strip() for l in sys.stdin if l.strip()]
delims = {'(': ')', '[': ']', '{': '}', '<': '>'}
closes = set(delims.values())
scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
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

score = 0
for i, l in enumerate(lines):
    print(i, end=' ')
    res = parse(l)
    if res[0] is True:
        print('OK')
    elif res[0] is BAD:
        _, op, cl = res
        sc = scores[cl]
        score += sc
        print(f'Bad: opened {op}, closed {cl}, score {sc}')
    elif res[0] is INCOMP:
        _, stk = res
        print(f'Incomp: needs {stk}')
    else:
        assert False
print(f'Score: {score}')
