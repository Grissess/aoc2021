import sys
cols = list(zip(*[line.strip() for line in sys.stdin]))
bits = ''.join('1' if col.count('1') > col.count('0') else '0' for col in cols)
negbits = ''.join('0' if bit == '1' else '1' for bit in bits)
gamma, epsilon = int(bits, 2), int(negbits, 2)
print(bits, negbits, gamma, epsilon, gamma*epsilon)
