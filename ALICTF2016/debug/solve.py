from z3 import *
import os
import string
from struct import pack, unpack
charset = string.ascii_lowercase + string.digits
def solv(result, v5, v3):
	solver = Solver()
	for i in range(0, 1):
		globals()['b%i' % i] = BitVec('b%i' % i, 32)
	
	v7 = 0x112233
	v8 = 0x44556677
	v9 = 0x8899aabb
	v10 = 0xccddeeff
	
	solver.add(b0 + ((v3 + result) ^ (v9 +(16 * result)) ^ (v10 + (result >> 5))) == v5)
	solver.check()
	modl = solver.model()
	obj = globals()['b%i' % i]
	c = modl[obj].as_long()
	
	v5 = c & 0xffffffff
	solver = Solver()
	for i in range(0, 1):
		globals()['b%i' % i] = BitVec('b%i' % i, 32)
	v7 = 0x112233
	v8 = 0x44556677
	v9 = 0x8899aabb
	v10 = 0xccddeeff

	solver.add(b0 + ((v3 + v5) ^ (v7 + (16 * v5)) ^ (v8 + (v5 >> 5))) == result)
	solver.check()
	modl = solver.model()
	obj = globals()['b%i' % i]
	c = modl[obj].as_long()
	result = c
	v3 = (v3 + 0x61c88647) & 0xffffffff

	return (result, v5, v3)
	
v3 = 0 
for i in range(128):
	v3 = (v3 - 0x61c88647) & 0xffffffff
res = 0xdc26ce6c ^ 0x31313131
v5 = 0xd8b6c625 ^ 0x31313131
for i in range(128):
	(res,v5,v3) = solv(res, v5, v3)

print hex(res), hex(v5)
des = [res, v5]
v3 = 0 
for i in range(128):
	v3 = (v3 - 0x61c88647) & 0xffffffff
res = 0xed907319 ^ 0x31313131
v5 = 0x03c6a63b ^ 0x31313131
for i in range(128):
	(res,v5,v3) = solv(res, v5, v3)
	
print hex(res), hex(v5)
des.append(res)
des.append(v5)

input  = ""
for i in des:
        input +=hex(i)[2:-1]

print input
#c6bf3d7cdad82ea712cea62cccbafddf



	
