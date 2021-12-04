import sys
words = [line.strip() for line in sys.stdin]
cols = list(zip(*words))
bits = ''.join('1' if col.count('1') >= col.count('0') else '0' for col in cols)
negbits = ''.join('0' if bit == '1' else '1' for bit in bits)
gamma, epsilon = int(bits, 2), int(negbits, 2)
soxy, sco = set(words), set(words)
for i in range(len(words[0])):
    if len(soxy) > 1:
        major = len([x for x in soxy if x[i] == '1']) >= len([x for x in soxy if x[i] == '0'])
        bit = '1' if major else '0'
        soxy = {x for x in soxy if x[i] == bit}
    if len(sco) > 1:
        major = len([x for x in sco if x[i] == '1']) >= len([x for x in sco if x[i] == '0'])
        bit = '0' if major else '1'
        sco = {x for x in sco if x[i] == bit}
oxy, co = int(list(soxy)[0], 2), int(list(sco)[0], 2)
print(bits, negbits, gamma, epsilon, gamma*epsilon)
print(oxy, co, oxy * co)
