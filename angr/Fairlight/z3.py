from z3 import *

s = Solver()

c = [BitVec("c%02d" % i, 8) for i in xrange(14)]

s.add(((c[5] ^ c[9]) + c[11])*c[0] -2744 == c[13])
s.add((c[13] ^ c[4])-c[11]+c[1] -33 == c[11])
s.add((c[8]^c[11]) +c[13] + c[2] - 194 == c[4])
s.add((c[0] ^ c[13]) + c[2] + c[3] - 229 == c[0])
s.add((c[5]^c[8]) + c[6] + c[4] - 115 == c[12])
s.add((c[10]^c[12]) + c[8] + c[5] - 102 == c[9])
s.add((c[13]^c[7]) + c[2] + c[6] - 168 == c[10])
s.add((c[9]^c[5]) + c[10] + c[7] -62 == c[8])
s.add((c[2]^c[6]) + c[13] + c[8] - 176 == c[7])
s.add((c[12]^c[5]) + c[10] + c[9] - 115 == c[6])
s.add((c[11]^c[1]) + c[8] + c[10] -208 == c[5])
s.add(c[11] + (c[12] ^c[1]) - c[8] +c[1] + c[6] -59 == c[4])
s.add(c[12] + (c[9] ^ c[4]) - c[3] + c[1] -c[0] +52 == c[3])
s.add(c[13] +c[12] - (c[8]^c[2]) + c[4] - c[1] - 115 == c[1])

if s.check() == sat:
    m = s.model()
    res = ""
    for i in xrange(14):
        res += chr(int(str(m[c[i]])))
    print res
