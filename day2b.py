import sys, functools
cmds = [(lambda cmd, _, val: (cmd, int(val)))(*x.partition(' ')) for x in sys.stdin]
fwd, dp, aim = functools.reduce(
        lambda st, cmd: (lambda fwd, dp, aim, cmd, val:\
                (fwd+val, dp+val*aim, aim) if cmd == 'forward' else\
                (fwd, dp, aim+val) if cmd == 'down' else\
                (fwd, dp, aim-val) # if cmd == 'up'
        )(*st, *cmd),
        cmds,
        (0, 0, 0)
)
print(fwd, dp, aim, fwd * dp)
