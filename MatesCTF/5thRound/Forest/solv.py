from z3 import *
import os

def solv(a,b,c,d,e):
    solver = Solver()

    for i in range(0, 4):
        globals()['b%i' % i] = BitVec('b%i' % i, 8)

    solver.add(0x33*b0+0x7B*b1+0x67*b2+0xBB*b3 == a)
    solver.add(0x5A*b0+0x81*b1+0xCA*b2+0x7F*b3 == b)
    solver.add(0x87*b0+0xFA*b1+0x83*b2+0x27*b3 == c)
    solver.add(0x06*b0+0xC6*b1+0x73*b2+0xC2*b3 == d)
    solver.add(0x09*b0+0x82*b1+0x1C*b2+0x1B*b3 == e)

    solver.check()
    modl = solver.model()
    result = []
    for i in range(0,4):
        obj = globals()['b%i' % i]
        c = modl[obj].as_long()
        result.append(c)
    return result
    
byte0 = solv(0x11f3e, 0x14b3c, 0x133f9, 0x14ba7, 0x763a)
byte1 = solv(0x738f, 0x98bb, 0x8e08, 0x866a, 0x3210)
byte2 = solv(0xdcac, 0xebf4, 0xb828, 0xf130, 0x4430)
byte3 = solv(0x2abd, 0x271e, 0x2e21, 0x31df, 0x145e)

for i in range(4):
    print byte0[i] ^ (byte1[i] << 8) ^ (byte2[i] << 16) ^ (byte3[i] << 24)
