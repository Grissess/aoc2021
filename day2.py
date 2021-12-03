import sys
cmds = [(lambda cmd, _, val: (cmd, int(val)))(*x.partition(' ')) for x in sys.stdin]
fwd = sum(val for cmd, val in cmds if cmd == 'forward')
dp = sum(val for cmd, val in cmds if cmd == 'down') - sum(val for cmd, val in cmds if cmd == 'up')
print(fwd, dp, fwd * dp)
